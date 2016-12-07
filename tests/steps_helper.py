def adding_show_steps(driver):
    add_show_page = driver.tap_on_floating_plus()
    show_name, widget = add_show_page.tap_on_selected_show()
    widget.add_show(show_name)
    driver.func_buttons.press_back_button()


def open_statistics_steps(driver):
    menu_bar_frame = driver.top_layout.open_menu_bar()
    statistics_page = menu_bar_frame.tap_on_statistics()
    return statistics_page
