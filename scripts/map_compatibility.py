"""Ensure appended maps never renumber any preceding group or map."""
def assert_map_prefix(current,old):
 assert current.keys()==old.keys()
 for key,value in old.items():
  if key=='gMapGroup_Europe':assert current[key][:len(value)]==value
  else:assert current[key]==value,key
