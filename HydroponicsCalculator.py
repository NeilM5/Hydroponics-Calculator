import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="Hydroponics Calculator", width=600, height=500, resizable=True)

plant_type_dict = {
    # [Target EC, Target pH]
    "Lettuce": [1, 6],
    "Tomato": [3.5, 5.8],
    "Cucumber": [2.1, 5.9]
}

water_type_dict = {
    "Tap Water": 7.5,
    "RO": 6.3, 
    "Rainwater": 5.8,
}

def nutrientQuant():
    res_size = dpg.get_value("RS")
    tg_ec = dpg.get_value("TEC")
    bs_ec = dpg.get_value("BEC")

    ec_inc = tg_ec - bs_ec
    nutri_quantity = (ec_inc * res_size) / 0.1

    dpg.add_text(f"{round(nutri_quantity, 1)} grams", parent="OPTN")

def pHLevel():
    res_size = dpg.get_value("RS")
    tg_ph = dpg.get_value("TPH")
    ct_ph = dpg.get_value("CPH")
    st_fact = dpg.get_value("SF")

    if st_fact == 0.0:
        dpg.add_text("Strenght Factor cannot be 0", wrap=120, parent="OPTP")

    ph_change = tg_ph - ct_ph
    ph_solution = (ph_change * res_size) / st_fact

    d_or_u = ""
    if ph_solution < 0:
        d_or_u = "pH Down"
    if ph_solution > 0:
        d_or_u = "pH Up"

    dpg.add_text(f"{round(abs(ph_solution), 1)} mL {d_or_u}", parent="OPTP")

def setPlantValues(sender, data):
    plant_select = dpg.get_value(sender)
    if plant_select in plant_type_dict:
        dpg.set_value("TEC", plant_type_dict[plant_select][0])
        dpg.set_value("TPH", plant_type_dict[plant_select][1])

def setWaterValues(sender, data):
    water_select = dpg.get_value(sender)
    if water_select in water_type_dict:
        dpg.set_value("CPH", water_type_dict[water_select])

def clearItems():
    dpg.delete_item("OPTN", children_only=True)
    dpg.delete_item("OPTP", children_only=True)

with dpg.window(label="Input", tag="INP", width=250, height=440, no_resize=True, no_collapse=True, no_move=True, no_close=True):
    # Plant Inputs
    dpg.add_combo(items=list(plant_type_dict.keys()), label="Plant Type", width=100, callback=setPlantValues)
    dpg.add_combo(items=("Seedling", "Vegetative", "Flowering"), label="Growth Stage", width=100)
    dpg.add_input_int(label="Plant Count", min_value=0, min_clamped=True, width=100, step=0, default_value=0)

    # Unholy amount of spacing
    dpg.add_spacer()
    dpg.add_spacer()
    dpg.add_spacer()
    dpg.add_spacer()

    # Water Input
    dpg.add_input_int(label="Resevoir Size (L)", tag="RS", min_value=0, min_clamped=True, width=100, step=0, default_value=0)
    dpg.add_input_float(label= "Target (EC)", tag="TEC", min_value = 0, min_clamped=True, format="%.1f", width=100, step=0, default_value=0)
    dpg.add_input_float(label= "Base (EC)", tag="BEC", min_value = 0, min_clamped=True, format="%.1f", width=100, step=0, default_value=0)
    dpg.add_combo(items=list(water_type_dict.keys()), label="Water Type", width=100, callback=setWaterValues)
    dpg.add_input_float(label="Current pH", tag="CPH", min_value=0, min_clamped=True, max_value=14, max_clamped=True, step=0, format="%.1f", width=100)
    dpg.add_input_float(label="Target pH", tag="TPH", min_value=0, min_clamped=True, max_value=14, max_clamped=True, step=0, format="%.1f", width=100)
    dpg.add_input_float(label="Strength Factor", tag="SF", min_value=0, min_clamped=True, max_value=14, max_clamped=True, step=0, format="%.1f", width=100)

with dpg.window(label="Output", tag="OPT", width=305, height=280, no_resize=True, no_collapse=True, no_move=True, no_close=True):
    with dpg.child_window(width=140, height=150, pos=(10, 30), tag="OPTN"):
        pass
    with dpg.child_window(width=140, height=150, pos=(155, 30), tag="OPTP"):
        pass

    dpg.add_button(label="Calculate Nutrient Quantity", width=200, pos=(10, 190), callback=nutrientQuant)
    dpg.add_button(label="Calculate pH Level", width=200, pos=(10, 220), callback=pHLevel)
    dpg.add_button(label="Clear", width=100, pos=(10, 250), callback=clearItems)

dpg.set_item_pos("INP", pos=(10, 10))
dpg.set_item_pos("OPT", pos=(270, 10))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context() 