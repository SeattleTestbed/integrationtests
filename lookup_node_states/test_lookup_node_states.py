"""
<Program>
  test_lookup_node_states.py

<Purpose>
  use advertise.repy to do a lookup for nodes in the four
  differe states: acceptdonation, canonical, twopercent
  and movingto_twopercent. And send out notifications
  if the number of nodes in each state is not what is expected.

<Started> 
  August 5, 2009

<Author>
  Monzur Muhammad
  monzum@cs.washington.edu
"""

# We'll search for nodestate keys in this directory
keys_dir = "/home/integrationtester/cron_tests/lookup_node_states/"

# Notification levels.
# We don't want to have too many nodes in transient states (as that means 
# the clearinghouse hasn't been able to contact them and set them up).
max_acceptdonation_nodes = 50 
max_canonical_nodes = 50 
max_movingtotwopercent = 20

# For correctly set up nodes, we warn about too low numbers.
min_twopercent_nodes = 300 


import integrationtestlib
import send_gmail

from repyportability import *
add_dy_support(locals())
rsa = dy_import_module('rsa.r2py')
advertise = dy_import_module('advertise.r2py')


# Get all public keys for different states from file
twopercentpublickey = rsa.rsa_file_to_publickey(keys_dir + "twopercent.publickey")
canonicalpublickey = rsa.rsa_file_to_publickey(keys_dir + "canonical.publickey")
acceptdonationpublickey = rsa.rsa_file_to_publickey(keys_dir + "acceptdonation.publickey")
movingtotwopercentpublickey = rsa.rsa_file_to_publickey(keys_dir + "movingto_twopercent.publickey")

important_node_states = [('twopercent', twopercentpublickey), 
    ('canonical', canonicalpublickey), 
    ('acceptdonation', acceptdonationpublickey), 
    ('movingto_twopercent', movingtotwopercentpublickey),
    ] 



# Exception raised if AdvertiseLookup fails somehow
class AdvertiseLookup(Exception):
  pass



def check_nodes():
  """
  <Purpse>
    Check for nodes advertising on the advertise services, and 
    find nodes in different states.

  <Arguments>
    None.

  <Exception>
    AdvertiseLookup - raised if advertise_lookup gives an error.

  <Side Effects>
    None

  <Return>
    None 
  """
  total_nodes = 0
  node_result = {}
  integrationtestlib.log("Starting advertise_lookup()")

  # Go through all the possible node states and do an advertise lookup
  for node_state_name, node_state_pubkey in important_node_states:
    integrationtestlib.log("Printing " + node_state_name + " nodes:")

    # Retrieve node list from advertise services
    try:
      node_list = advertise.advertise_lookup(node_state_pubkey, maxvals = 10*1024*1024)
    except Exception, e:
      raise AdvertiseLookup("advertise_lookup() failed with " + 
          repr(e) + " when looking up key " + 
          rsa.rsa_publickey_to_string(node_state_pubkey))

    # Keep track of total nodes
    total_nodes += len(node_list)
    
    node_result[node_state_name] = len(node_list)

    # Log all the node lookup info
    for node in node_list:
      print node

  node_result['Total nodes'] = total_nodes
  return node_result   




def main():
  """
  <Purpose>
    Call check_nodes and then notify developers if result is unusual.

  <Exceptions>
    None

  <Side Effects>
    May send out a notification email.

  <Return>
    None
  """
  # Setup the gmail lib for sending notification
  success, explanation_str = send_gmail.init_gmail()

  if not success:
    integrationtestlib.log(explanation_str)
    sys.exit(0)

  notification_subject = "test_lookup_node_states() failed"

  results = check_nodes()
  integrationtestlib.log("Lookup results: "+ str(results))

  # Check to see if any of the results is not normal, and 
  # send notifications accordingly.
  message = "Too many nodes in state " 
  if results['acceptdonation'] > max_acceptdonation_nodes:
    message += "acceptdonation: " +  str(results['acceptdonation'])
  elif results['canonical'] > max_canonical_nodes:
    message += "canonical: " + str(results['canonical'])

  if results['twopercent'] < min_twopercent_nodes:
    message = "Too few nodes in state twopercent: " + str(results['twopercent'])

  message += "\nLookup results:\n" + str(results)
  print message
  integrationtestlib.notify(message, notification_subject)



if __name__ == "__main__":
  main()

