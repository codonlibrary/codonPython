import platform
from dataclasses import dataclass
from datetime import datetime
from .exceptions import (
    MESHAuthenticationError,
    MESHDownloadErrors,
    MESHInvalidRecipient,
    MESHMessageAlreadyDownloaded,
    MESHMessageMissing,
    MESHMultipleMatches,
    MESHUnknownError,
)
from gzip import compress, decompress
from hashlib import md5
from hmac import new as hmac
from math import ceil
from os import path
from uuid import uuid4
import logging
from typing import Generator, Union

import requests as r


@dataclass
class MESHConnection:
    """Class for handling MESH API interactions.
    
    Parameters
    ----------
    mailbox : string
        The MESH ID of the mailbox this client is for
    password : string
        The password to this mailbox
    api_shared_key : string
        The shared API key for the MESH environment the mailbox is in
    cert_loc : string
        Path to the MESH API certificate location
    key_loc : string
        Path to the MESH API certificate private key location
    base_ca_loc : string
        Path to the base MESH certificate authority certificate bundle.
        Set to False to disable inbound SSL checks if necessary
    root_url : string
        Root MESH URL. Default value is the live MESH service
    org : string
        Organisation name. Default value NHS Digital
    """

    mailbox: str
    password: str
    api_shared_key: str
    cert_loc: str
    key_loc: str
    base_ca_loc: str
    root_url: str = "https://mesh-sync.national.ncrs.nhs.uk"
    org: str = "NHS Digital"

    def check_authentication(self) -> bool:
        """
        Check authentication with the MESH API.
        This should be done at the start of any session (per the API docs)
            
        Returns
        ----------
        bool
            indicates if authentication was successful or not
        
        Raises
        ----------
        MESHUnknownError
            There was an unexpected return status from the MESH API
        
        Examples
        ----------
        >>> client.check_authentication()
        True
        """
        resp = r.post(
            f"{self.root_url}/messageexchange/{self.mailbox}",
            headers={
                "Authorization": generate_authorization(
                    self.mailbox, self.password, self.api_shared_key
                ),
                "Mex-ClientVersion": f"pyMESHAPI0.1a",
                "Mex-OSArchitecture": platform.machine(),
                "Mex-OSName": platform.system(),
                "Mex-OSVersion": platform.version(),
            },
            cert=(self.cert_loc, self.key_loc),
            verify=self.base_ca_loc,
        )
        if resp.status_code == 403:
            return False
        if resp.status_code == 200:
            return True
        raise MESHUnknownError

    def send_file(
        self,
        dest_mailbox: str,
        message_location: str,
        workflow_id: str,
        message_subject: str = None,
        message_id: str = None,
        process_id: str = None,
        compress_message: bool = True,
        encrypted: bool = False,
    ):
        """
        Send a file to the MESH API.
        This will automatically chunk the message if required, splitting into chunks at 80MB (MESH API has a
        chunk size limit of 100MB). If required, this will also compress the message before transmission using
        gzip.
        
        Parameters
        ----------
        dest_mailbox : string
            MESH Mailbox ID of the recipient
        message_location : string
            Path to the readable file to send as a message
        workflow_id : string
            DTS Workflow ID
        message_subject : string
            Optional subject line to use for the message, for SMTP (email) messages.
        message_id : string
            Optional local identifier for the message. Required to track the message later.
        process_id : string
            Optional process ID for the MESH message. Currently not used.
        compress_message : boolean
            Indicates if the message should be encrypted. If true (default), then the message will be compressed
            using gzip before sending to MESH.
        encrypted : boolean
            Indicates if the file to send has been encrypted. This is solely used to pass a flag to MESH
            and does not encrypt the file or otherwise alter processing.
            
        Returns
        ----------
        dict
            key 'messageID', holding value of the MESH internal ID assigned to the sent message
        
        Raises
        ----------
        MESHAuthenticationError
            There was an authentication error accessing this page. Either the SSL certificate used is invalid,
            or the client provided the wrong Mailbox ID, Password, or Shared Key.
        MESHInvalidRecipient
            The mailbox ID provided is not a valid recipient for this message
        MESHUnknownError
            There was an unexpected return status from the MESH API
        
        Examples
        ----------
        >>> client.send_file("TEST", 'c:/test/test.txt', 'test_flow')
        {'messageID': '20200211115928515346_9359E2'}
        """
        with open(message_location, "rb") as file:
            message = file.read()
        filename = path.basename(message_location)
        return self.send_message(
            dest_mailbox=dest_mailbox,
            message=message,
            filename=filename,
            workflow_id=workflow_id,
            message_subject=message_subject,
            message_id=message_id,
            process_id=process_id,
            compress_message=compress_message,
            encrypted=encrypted,
        )

    def send_message(
        self,
        dest_mailbox: str,
        message: bytes,
        filename: str,
        workflow_id: str,
        message_subject: str = None,
        message_id: str = None,
        process_id: str = None,
        compress_message: bool = True,
        encrypted: bool = False,
    ):
        """
        Send a message to the MESH API.
        This will automatically chunk the message if required, splitting into chunks at 80MB (MESH API has a
        chunk size limit of 100MB). If required, this will also compress the message before transmission using
        gzip.
        
        Parameters
        ----------
        dest_mailbox : string
            MESH Mailbox ID of the recipient
        message : bytes
            Bytes representation of the file to transmit
        filename : string
            Original filename for the message being transmitted
        workflow_id : string
            DTS Workflow ID
        message_subject : string
            Optional subject line to use for the message, for SMTP (email) messages.
        message_id : string
            Optional local identifier for the message. Required to track the message later.
        process_id : string
            Optional process ID for the MESH message. Currently not used.
        compress_message : boolean
            Indicates if the message should be encrypted. If true (default), then the message will be compressed
            using gzip before sending to MESH.
        encrypted : boolean
            Indicates if the message being sent has been encrypted. This is solely used to pass a flag to MESH
            and does not encrypt the message or otherwise alter processing.
            
        Returns
        ----------
        dict
            key 'messageID', holding value of the MESH internal ID assigned to the sent message
        
        Raises
        ----------
        MESHAuthenticationError
            There was an authentication error accessing this page. Either the SSL certificate used is invalid,
            or the client provided the wrong Mailbox ID, Password, or Shared Key.
        MESHInvalidRecipient
            The mailbox ID provided is not a valid recipient for this message
        MESHUnknownError
            There was an unexpected return status from the MESH API
        
        Examples
        ----------
        >>> client.send_message("TEST", b'test', 'test.txt', 'test_flow')
        {'messageID': '20200211115928515346_9359E2'}
        """
        checksum = md5(message).hexdigest()
        if compress_message:
            message = compress(message)

        headers = {
            "Authorization": generate_authorization(
                self.mailbox, self.password, self.api_shared_key
            ),
            "Content-Type": "application/octet-stream",
            "Mex-From": self.mailbox,
            "Mex-To": dest_mailbox,
            "Mex-WorkflowID": workflow_id,
            "Mex-Filename": filename,
            "Mex-MessageType": "DATA",
            "Mex-Version": "1.0",
            "Mex-Checksum": f"md5 {checksum}",
        }

        if process_id is not None:
            headers["Mex-ProcessID"] = process_id
        if message_id is not None:
            headers["Mex-LocalID"] = message_id
        if compress_message:
            headers["Mex-Content-Compressed"] = "1"
            headers["Content-Encoding"] = "gzip"
        if encrypted:
            headers["Mex-Content-Encrypted"] = "1"
        if message_subject is not None:
            headers["Mex-Subject"] = message_subject
        if len(message) > 80000000:
            headers["Mex-Chunk-Range"] = f"1:{ceil(len(message)/80000000)}"

        if len(message) > 80000000:
            resp = r.post(
                url=f"{self.root_url}/messageexchange/{self.mailbox}/outbox",
                data=message[0:80000000],
                headers=headers,
                cert=(self.cert_loc, self.key_loc),
                verify=self.base_ca_loc,
            )
            if resp.status_code == 403:
                raise MESHAuthenticationError
            if resp.status_code == 417:
                raise MESHInvalidRecipient
            if resp.status_code != 202:
                raise MESHUnknownError
            message_id = resp.json()["messageID"]
            for chunk in range(2, ceil(len(message) / 80000000) + 1):
                self.send_message_chunk(
                    message_id=message_id,
                    message_chunk=message[(chunk - 1) * 80000000 : chunk * 80000000],
                    chunk_no=chunk,
                    chunk_range=ceil(len(message) / 80000000),
                    compressed=compress_message,
                )
        else:
            resp = r.post(
                url=f"{self.root_url}/messageexchange/{self.mailbox}/outbox",
                data=message,
                headers=headers,
                cert=(self.cert_loc, self.key_loc),
                verify=self.base_ca_loc,
            )
            if resp.status_code == 403:
                raise MESHAuthenticationError
            if resp.status_code == 417:
                raise MESHInvalidRecipient
            if resp.status_code != 202:
                raise MESHUnknownError

        return resp.json()

    def send_message_chunk(
        self,
        message_id: str,
        message_chunk: bytes,
        chunk_no: int,
        chunk_range: int,
        compressed: bool = True,
    ) -> None:
        """
        Send a message chunk to the MESH API.
        This is expected to only be called by the send_message method.
        
        Parameters
        ----------
        message_id : string
            The internal MESH ID of the message to upload a chunk for
        message_chunk : bytes
            The data to send in this chunk
        chunk_no : integer
            The number of the chunk to upload
        chunk_range : integer
            How many chunks there are to upload in total
        compressed : boolean
            Default True. Is the message compressed?
        
        Raises
        ----------
        MESHAuthenticationError
            There was an authentication error accessing this page. Either the SSL certificate used is invalid,
            or the client provided the wrong Mailbox ID, Password, or Shared Key.
        MESHUnknownError
            There was an unexpected return status from the MESH API
        
        Examples
        ----------
        >>> client.send_message_chunk("20200211115754892283_BC7B68", b'test', 2)
        """
        headers = {
            "Authorization": generate_authorization(
                self.mailbox, self.password, self.api_shared_key
            ),
            "Mex-From": self.mailbox,
            "Content-Type": "application/octet-stream",
            "Mex-Chunk-Range": f"{chunk_no}:{chunk_range}",
        }
        if compressed:
            headers["Content-Encoding"] = "gzip"
        resp = r.post(
            url=f"{self.root_url}/messageexchange/{self.mailbox}/outbox/{message_id}/{chunk_no}",
            data=message_chunk,
            headers=headers,
            cert=(self.cert_loc, self.key_loc),
            verify=self.base_ca_loc,
        )
        if resp.status_code == 403:
            raise MESHAuthenticationError
        if resp.status_code != 202:
            raise MESHUnknownError

    def check_message_status(self, message_id: str) -> dict:
        """
        Check status of a sent message.
        
        Parameters
        ----------
        message_id : string
            The local message ID, eg. as provided to send_message. Does NOT work with MESH Message IDs, only
            the local ID optionally provided on sending the message.
        
        Returns
        ----------
        dict
            The full response from the MESH API for this local ID. For details, consult the MESH API documentation
        
        Raises
        ----------
        MESHAuthenticationError
            There was an authentication error accessing this page. Either the SSL certificate used is invalid,
            or the client provided the wrong Mailbox ID, Password, or Shared Key.
        MESHMultiplematches
            There are multiple messages in the outbox with this local ID
        MESHUnknownError
            There was an unexpected return status from the MESH API
        
        Examples
        ----------
        >>> client.check_message_status(test)
        {"statusSuccess": ...}
        """
        resp = r.get(
            url=f"{self.root_url}/messageexchange/{self.mailbox}/outbox/tracking/{message_id}",
            headers={
                "Authorization": generate_authorization(
                    self.mailbox, self.password, self.api_shared_key
                )
            },
            cert=(self.cert_loc, self.key_loc),
            verify=self.base_ca_loc,
        )
        if resp.status_code == 403:
            raise MESHAuthenticationError
        # There is an error in the API itself - in case of multiple match, will send an error page with status 200 instead of 300
        if (resp.status_code == 300) or (
            resp.text
            == "<html><title>300: Multiple Choices</title><body>300: Multiple Choices</body></html>"
        ):
            raise MESHMultipleMatches
        if resp.status_code == 404:
            raise MESHMessageMissing
        if resp.status_code != 200:
            raise MESHUnknownError
        return resp.json()

    def check_and_download(
        self, save_folder: str = None, recursive: bool = True
    ) -> Union[Generator[dict, None, None], None]:
        """
        Download all messages in the inbox.
        This will automatically handle reconstructing chunked messages, and automatically decompress any messages
        which have Content-Encoding value of gzip.
        WARNING: each downloaded message will be fully reconstructed and decompressed if needed. This may cause
        issue for machines with very limited memory if there are very large files to download.
        
        If save_folder is provided, then downloaded files will be saved into that folder with their original filenames
        (and non-delivery receipts will be saved there). This may cause issue if there are multiple files with the
        same filename.
        
        If no save_folder is provided, then this function will return a generator which will yield each message in turn.
        When the generator yields a message, it will send an acknowledgement to the MESH API for the previous
        message; it is important that processing of the messages be complete and any required final outputs saved
        before this - once acknowledged a message cannot be downloaded from MESH again.
        
        Parameters
        ----------
        save_folder : string
            The folder to save the downloaded messages to. If None (default), then the files are not saved.
            The generator will only yield outputs if save_folder is not provided
        recursive : boolean
            If there are more than 500 messages in the inbox, should the method call itself recursively until the inbox
            is empty? The MESH API will only yield the first 500 messages in a call to fetch inbox contents; if set,
            this flag will ensure all messages are handled, if unset then the first 500 will be handled.
        
        Yields
        ----------
        dict
            If the message is a non delivery report, then the dict will have the key 'Non-Delivery',
                with value a dictionary of all message headers
            If the message is a data message, then the dict will have key equal to the FILENAME of
                the original file (as given by the Mex-FileName header), with value a dictionary with keys
                data (containing the bytes value of the message) and headers (containing all headers)
            
        Side Effects
        ----------
        For each message in the inbox,
        If the message is a non delivery report, then a file will be written to save_folder (if provided),
            with filename 'Non delivery report: (MESH message ID of failed delivery).txt', and with
            content 'Message not delivered. All known details below' followed by the full dictionary of
            headers from the download response
        If the message is a data message, then a file will be written to save_folder (if provided), with
            filename set to the FILENAME of the original file (as given by the Mex-FileName header), and
            content the (potentially reconstructed and/or decompressed) message body.
        
        Raises
        ----------
        MESHAuthenticationError
            There was an authentication error accessing the inbox. Either the SSL certificate used is invalid,
            or the client provided the wrong Mailbox ID, Password, or Shared Key.
        MESHUnknownError
            There was an unexpected return status from the MESH API when accessing the inbox
        MESHDownloadErrors
            There were errors during the download process. This exception has the attribute 'exceptions',
            which contains a full list of messages which generated exceptions, along with the exception.
            This is only raised after completion of all non-error downloads, and downloads which raise
            an exception are not acknowledged to the MESH API.
        
        Examples
        ----------
        >>> client.check_and_download("C:/Test Folder/")
        >>> for message in client.check_and_download():
        >>>     print(message)
        {'test.txt': b'test_message'}
        {'test2.txt': b'test_message_2'}
        """
        if save_folder is None:
            return self._check_download_generator(recursive)
        else:
            self._check_download_save(save_folder, recursive)

    def _check_download_generator(self, recursive: bool) -> Generator[dict, None, None]:
        """Internal only - generator to return for check_and_download"""
        message_ids = self.check_inbox()
        exceptions = []
        if recursive:
            repeat_needed = self.check_inbox_count() > 500
        for message_id in message_ids:
            try:
                yield self.download_message(message_id, save_folder=None)
            except Exception as e:
                exceptions.append((message_id, e))
            else:
                self.ack_download_message(message_id)
        # Force termination if there are enough messages failing to download that they fill the inbox
        # Reduces risk of infinite loops
        if len(exceptions) >= 500:
            raise MESHDownloadErrors(exceptions)
        if recursive and repeat_needed:
            try:
                for msg in self._check_download_generator(recursive=True):
                    yield msg
            except MESHDownloadErrors as e:
                exceptions.extend(e.exceptions)
        if exceptions:
            raise MESHDownloadErrors(exceptions)

    def _check_download_save(self, save_folder: str, recursive: bool) -> None:
        """Internal only - function to save results for check_and_download"""
        message_ids = self.check_inbox()
        exceptions = []
        if recursive:
            repeat_needed = self.check_inbox_count() > 500
        for message_id in message_ids:
            try:
                self.download_message(message_id, save_folder)
            except Exception as e:
                exceptions.append((message_id, e))
            else:
                self.ack_download_message(message_id)
        # Force termination if there are enough messages failing to download that they fill the inbox
        # Reduces risk of infinite loops
        if len(exceptions) >= 500:
            raise MESHDownloadErrors(exceptions)
        if recursive and repeat_needed:
            try:
                self._check_download_save(save_folder, recursive=True)
            except MESHDownloadErrors as e:
                exceptions.extend(e.exceptions)
        if exceptions:
            raise MESHDownloadErrors(exceptions)

    def check_inbox(self) -> list:
        """
        Determine the MESH IDs of the contents of the inbox.
        This will return at most 500 entries, owing to the limitations of the API.
        
        Returns
        ----------
        list
            The MESH IDs of the messages in the inbox
        
        Raises
        ----------
        MESHAuthenticationError
            There was an authentication error accessing this page. Either the SSL certificate used is invalid,
            or the client provided the wrong Mailbox ID, Password, or Shared Key.
        MESHUnknownError
            There was an unexpected return status from the MESH API
        
        Examples
        ----------
        >>> client.check_inbox()
        ["20200211115754892283_BC7B68", "20200211115928515346_9359E2"]
        """
        resp = r.get(
            url=f"{self.root_url}/messageexchange/{self.mailbox}/inbox",
            headers={
                "Authorization": generate_authorization(
                    self.mailbox, self.password, self.api_shared_key
                )
            },
            cert=(self.cert_loc, self.key_loc),
            verify=self.base_ca_loc,
        )
        if resp.status_code == 403:
            raise MESHAuthenticationError
        if resp.status_code != 200:
            raise MESHUnknownError
        return resp.json()["messages"]

    def check_inbox_count(self) -> int:
        """
        Determine how many messages are in the MESH mailbox to download.
        
        Returns
        ----------
        int
            The number of messages ready to download
        
        Raises
        ----------
        MESHAuthenticationError
            There was an authentication error accessing this page. Either the SSL certificate used is invalid,
            or the client provided the wrong Mailbox ID, Password, or Shared Key.
        MESHUnknownError
            There was an unexpected return status from the MESH API
        
        Examples
        ----------
        >>> client.check_inbox_count()
        2
        """
        resp = r.get(
            url=f"{self.root_url}/messageexchange/{self.mailbox}/count",
            headers={
                "Authorization": generate_authorization(
                    self.mailbox, self.password, self.api_shared_key
                )
            },
            cert=(self.cert_loc, self.key_loc),
            verify=self.base_ca_loc,
        )
        if resp.status_code == 403:
            raise MESHAuthenticationError
        if resp.status_code != 200:
            raise MESHUnknownError
        return resp.json()["count"]

    def download_message(self, message_id: str, save_folder: str = None) -> dict:
        """
        Request a message from the MESH API.
        This will automatically handle reconstructing chunked messages, and automatically decompress any messages
        which have Content-Encoding value of gzip.
        WARNING: the full, reconstructed message will be held in memory, including after decompression. This may
        cause problems, if you are using the API to download very large files on a machine with very limited memory.
        
        Parameters
        ----------
        message_id : string
            The internal MESH ID of the message to download
        save_folder : string
            The folder to save the downloaded message to. If None (default), then the files are not saved.
        
        Returns
        ----------
        dict
            If the message is a non delivery report, then the dict will have the key 'Non-Delivery',
                with value a dictionary of all message headers
            If the message is a data message, then the dict will have key equal to the FILENAME of
                the original file (as given by the Mex-FileName header), with value a dictionary with keys data
                (holding the message contents) and headers (holding all headers from the original response)
            
        Side Effects
        ----------
        If the message is a non delivery report, then a file will be written to save_folder (if provided),
            with filename 'Non delivery report: (MESH message ID of failed delivery).txt', and with
            content 'Message not delivered. All known details below' followed by the full dictionary of
            headers from the download response
        If the message is a data message, then a file will be written to save_folder (if provided), with
            filename set to the FILENAME of the original file (as given by the Mex-FileName header), and
            content the (potentially reconstructed and/or decompressed) message body.
        
        Raises
        ----------
        MESHAuthenticationError
            There was an authentication error accessing this page. Either the SSL certificate used is invalid,
            or the client provided the wrong Mailbox ID, Password, or Shared Key.
        MESHMessageMissing
            There is no message with the provided message ID in the mailbox
        MESHMessageAlreadyDownloaded
            The message with the provided message ID has already been downloaded and acknowledged
        MESHUnknownError
            There was an unexpected return status from the MESH API
        
        Examples
        ----------
        >>> client.download_message("20200211115754892283_BC7B68", "C:/Test Folder/")
        {'test.txt': b'test_message'}
        >>> client.download_message("20200211115754892283_BC7B69")
        {'Non-Delivery': {(significant list of headers)}}
        """
        resp = r.get(
            url=f"{self.root_url}/messageexchange/{self.mailbox}/inbox/{message_id}",
            headers={
                "Authorization": generate_authorization(
                    self.mailbox, self.password, self.api_shared_key
                ),
                "Accept-Encoding": "gzip",
            },
            cert=(self.cert_loc, self.key_loc),
            verify=self.base_ca_loc,
            stream=True,
        )
        if resp.status_code == 403:
            raise MESHAuthenticationError
        elif resp.status_code == 404:
            raise MESHMessageMissing
        elif resp.status_code == 410:
            raise MESHMessageAlreadyDownloaded
        elif resp.status_code == 206:
            core_data = resp.raw.data
            chunk_count = int(resp.headers["Mex-Chunk-Range"][2:])
            for chunk in range(2, chunk_count + 1):
                core_data += self.download_message_chunk(message_id, chunk)
        elif resp.status_code == 200:
            core_data = resp.raw.data
        else:
            raise MESHUnknownError

        # If this header exists, the message is a non delivery report
        if ("LinkedMessageId" in resp.headers) or (
            resp.headers["Mex-MessageType"] == "REPORT"
        ):
            logging.info(
                f"Non delivery report for message {resp.headers['LinkedMessageId']}"
            )
            if save_folder is not None:
                with open(
                    path.join(
                        save_folder,
                        f"Non delivery report: {resp.headers['LinkedMessageId']}.txt",
                    ),
                    "w",
                ) as file:
                    file.write(
                        "Message not delivered. All known details below\n"
                        + str(resp.headers)
                    )
            return {"Non-Delivery": resp.headers}

        if ("Content-Encoding" in resp.headers) and (
            resp.headers["Content-Encoding"] == "gzip"
        ):
            core_data = decompress(core_data)

        if save_folder is not None:
            with open(
                path.join(save_folder, resp.headers["Mex-Filename"]), "wb"
            ) as file:
                file.write(core_data)
        return {
            resp.headers["Mex-Filename"]: {"data": core_data, "headers": resp.headers}
        }
        # CASES:
        # Message is complete and is a non delivery report
        #   log the non delivery report, create message in folder

    def download_message_chunk(self, message_id: str, chunk_no: int) -> bytes:
        """
        Request a message chunk from the MESH API.
        This is expected to only be called by the download_message method.
        
        Parameters
        ----------
        message_id : string
            The internal MESH ID of the message to download a chunk from
        chunk_no : integer
            The number of the chunk to download
        
        Returns
        ----------
        bytes
            The raw content of the downloaded chunk
        
        Raises
        ----------
        MESHAuthenticationError
            There was an authentication error accessing this page. Either the SSL certificate used is invalid,
            or the client provided the wrong Mailbox ID, Password, or Shared Key.
        MESHMessageMissing
            There is no message with the provided message ID in the mailbox
        MESHMessageAlreadyDownloaded
            The message with the provided message ID has already been downloaded and acknowledged
        MESHUnknownError
            There was an unexpected return status from the MESH API
        
        Examples
        ----------
        >>> client.download_message_chunk("20200211115754892283_BC7B68", 1)
        b'test_message'
        """
        resp = r.get(
            url=f"{self.root_url}/messageexchange/{self.mailbox}/inbox/{message_id}/{chunk_no}",
            headers={
                "Authorization": generate_authorization(
                    self.mailbox, self.password, self.api_shared_key
                ),
                "Accept-Encoding": "gzip",
            },
            cert=(self.cert_loc, self.key_loc),
            verify=self.base_ca_loc,
            stream=True,
        )
        if resp.status_code == 403:
            raise MESHAuthenticationError
        elif resp.status_code == 404:
            raise MESHMessageMissing
        elif resp.status_code == 410:
            raise MESHMessageAlreadyDownloaded
        elif resp.status_code in (200, 206):
            return resp.raw.data
        else:
            raise MESHUnknownError

    def ack_download_message(self, message_id: str) -> None:
        """
        Send acknowledgement to the MESH API that a message has finished downloading.
        This should only be done after the message has successfully been saved - once sent, the message is remvoed from the MESH server.
        Per the API, this must be sent once a message has been successfully processed.
        
        Parameters
        ----------
        message_id : string
            The internal MESH ID of the downloaded message
        
        Returns
        ----------
        None
        
        Raises
        ----------
        MESHAuthenticationError
            There was an authentication error accessing this page. Either the SSL certificate used is invalid,
            or the client provided the wrong Mailbox ID, Password, or Shared Key.
        MESHUnknownError
            There was an unexpected return status from the MESH API
        
        Examples
        ----------
        >>> client.ack_download_message("20200211115754892283_BC7B68")
        """
        resp = r.put(
            url=f"{self.root_url}/messageexchange/{self.mailbox}/inbox/{message_id}/status/acknowledged",
            headers={
                "Authorization": generate_authorization(
                    self.mailbox, self.password, self.api_shared_key
                )
            },
            cert=(self.cert_loc, self.key_loc),
            verify=self.base_ca_loc,
        )
        if resp.status_code == 403:
            raise MESHAuthenticationError
        if resp.status_code != 200:
            raise MESHUnknownError


def generate_authorization(mailbox: str, password: str, api_shared_key: str) -> str:
    """
    Generate an authorization string as specified by the MESH API documentation v1.14
    
    Parameters
    ----------
    mailbox : string
        The mailbox ID to generate authorization for
    password : string
        The password for the mailbox
    api_shared_key : string
        The shared API key for the MESH environment the request is being made to
    
    Returns
    ----------
    string
        The generated authentication string
    
    Examples
    ----------
    >>> generate_authorization("TEST_BOX", "TEST_PW", "TEST_KEY")
    "NHSMESH TEST_BOX:ccd54b96-ee41-4d34-9700-7f9ec63d0720:1:202002120857:7632c7e908147f51f3d544209621f50126903779071417236428e47ea047872c"
    >>> generate_authorization("NEW_BOX", "NEW_PW", "TEST_KEY")
    "NHSMESH NEW_BOX:662c4ffa-c85c-4858-bae8-7327e09aeeb5:1:202002120858:7f1ef837210936a3125d24ae9d4e0e972079ed4a9ac6a4bf0b7bddb11cf20d95"
    """
    nonce = uuid4()
    time = datetime.now().strftime("%Y%m%d%H%M")
    hash_out = hmac(
        api_shared_key.encode(),
        msg=f"{mailbox}:{nonce}:1:{password}:{time}".encode("utf8"),
        digestmod="sha256",
    ).hexdigest()
    return f"NHSMESH {mailbox}:{nonce}:1:{time}:{hash_out}"
