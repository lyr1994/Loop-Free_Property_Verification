# Loop-Free_Property_Verification
##Experimental details

mininet ←-→  remote controller(POX controller)
Our work: modify POX controller to verify if loop exists when controller accept a rule

step 1: implement our verification module
step 2: modify ofp_flow_mod class in POX

inside POX:
create a message → fill message with forwarding rules →(our work: verify if there is loops → if no loop → ) send to switch

