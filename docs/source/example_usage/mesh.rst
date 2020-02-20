Use of the MESH API will generally follow one of a few standard patterns.

Upload file pattern:

* Check Authentication with the MESH API endpoint
* Send one or more files (chunked if needed)

.. code-block::

   from codonPython.mesh import MESHConnection
   mesh_client = MESHConnection(
       mailbox = 'test'
       password = 'test'
       api_shared_key = 'test'
       cert_loc = './certs/test.cert'
       key_loc = './certs/test.key'
       base_ca_loc = './certs/test.ca-bundle')
   
   if mesh_client.check_authentication():
       mesh_client.send_file('test_recipient', './test/test_20200224_1100.txt.dat', 'test_workflow')


Download file pattern:

* Check Authentication with the MESH API endpoint
* Request a list of files to download from the endpoint
* Download and process each in turn (downloading chunked files if needed)
* After each file has been *successfully* processed, send acknowledgement to the MESH API for that file
* Repeat as needed until there are no more files which can be processed. Note that the MESH API will return at most 500 message IDs at a time.

.. code-block::

   from codonPython.mesh import MESHConnection
   mesh_client = MESHConnection(
       mailbox = 'test'
       password = 'test'
       api_shared_key = 'test'
       cert_loc = './certs/test.cert'
       key_loc = './certs/test.key'
       base_ca_loc = './certs/test.ca-bundle')
   
   if mesh_client.check_authentication():
       # To save all messages to a folder
       mesh_client.check_and_download('./inbox')
       # To perform more complex processing on each
       for message in mesh_client.check_and_download():
           process(message)
       # To perform the flow manually instead of using the check_and_download helper method
       errors = []
       inbox_messages = mesh_client.check_inbox()
       for message_id in inbox_messages:
           try:
               message = mesh_client.download_message(message_id, './inbox')
               process(message)
               mesh_client.ack_download_message(message_id)
           except Exception as e:
               errors.append(e)


NB:
The regular MESH client has strict restrictions on filename and type. The API does not have any such restrictions, however it is likely that the system files are being sent to expects files to be in this format.
Unless you know otherwise files should be sent with .dat extension, with filename pattern Organisation_Date_Time.ext.dat where .ext is the original file extension.