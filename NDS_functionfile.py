# Nutrient Distribution System Function File
# Libraries
import numpy as np
import math

umbrella_shadow_width = 4.5     # metres
umbrella_shadow_length = 4.5    # metres
sensor_depth = 0.07             # metres
actuation_volume = umbrella_shadow_width * umbrella_shadow_length * sensor_depth
AVL = actuation_volume * 1000   # Convert to litres

mixing_tank_volume = 15.8       # Litres Changeable --> Adjusted for scaled prototype
volume_flow_rate = 2.5          # m/s Changeable --> Adjusted for scaled prototype

desired_pH = 6.5                # Changeable --> altered depending on ideal conditions for crop

# Function to calculate the duration of opening the servos for pH
def duration_pH(sensor_value):
    field_pH = sensor_value
    
    desired_Hplus_mols = (10**(-desired_pH)) * AVL
    desired_pOH_mols = 10 ** (14-desired_pH) * AVL
    field_Hplus_mols = (10**(-field_pH)) * AVL
    field_OH_mols = (10**(14-field_pH)) * AVL
    diff_Hplus_mols = desired_Hplus_mols - field_Hplus_mols
    
    if diff_Hplus_mols > 0:
        acid_additive_pH = 3    # Changeable
        req_mini_tank_Hplus_concentration = diff_Hplus_mols / mixing_tank_volume
        mini_tank_pH = -math.log10(req_mini_tank_Hplus_concentration)
        Hplus_conc_additive = 10 ** (-acid_additive_pH)
        volume_addition = diff_Hplus_mols/Hplus_conc_additive
        duration = volume_addition/volume_flow_rate
        return(duration)
    if diff_Hplus_mols < 0:
        base_additive_pH = 10.5
        req_mini_tank_Hplus_concentration = diff_Hplus_mols / mixing_tank_volume
        mini_tank_pH = -math.log10(req_mini_tank_Hplus_concentration)
        mini_tank_pOH = 14 - mini_tank_pH
        mini_tank_OH_conc = 10 ** (-mini_tank_pOH)
        OH_mols = mini_tank_OH_conc * mixing_tank_volume
        OH_conc_additive = 10 ** (-base_additive_pH)
        diff_OH_mols = desired_pOH - field_OH_mols
        
        
        
    else:
        print("No Actuation")



