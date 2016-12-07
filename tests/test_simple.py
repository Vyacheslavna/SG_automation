import tests.steps_helper as general


class TestSeriesGuide(object):
    def test_adding_show(self, main_shows_page):
        add_show_page = main_shows_page.tap_on_floating_plus()
        add_show_page.search_through_list()

        show_name, widget = add_show_page.tap_on_selected_show()
        widget.add_show(show_name)
        main_shows_page.func_buttons.press_back_button()

        series_name = main_shows_page.get_show_from_main_screen()
        assert show_name == series_name.get_attribute('text'), 'Show names does not match on main screen'

    def test_statistics(self, main_shows_page):
        statistics_page = general.open_statistics_steps(main_shows_page)
        start_number = statistics_page.get_number_of_shows()
        main_shows_page.func_buttons.press_back_button()

        general.adding_show_steps(main_shows_page)

        general.open_statistics_steps(main_shows_page)
        new_number = statistics_page.get_number_of_shows()
        assert start_number + 1 == new_number, \
            'Statistic number should be {inc_num}, but it is {new_number}'.format(inc_num=start_number + 1,
                                                                                  new_number=new_number)

    def test_watched_episode(self, main_shows_page):
        general.adding_show_steps(main_shows_page)

        statistics_page = general.open_statistics_steps(main_shows_page)
        watched_num = statistics_page.get_watched_number()
        main_shows_page.func_buttons.press_back_button()

        main_shows_page.top_layout.open_main_show_page()
        season, episode = main_shows_page.get_season_and_episode_number()
        episode_page = main_shows_page.tap_on_show()

        episode_page.set_episode_watched()
        main_shows_page.func_buttons.press_back_button()

        season_new, episode_new = main_shows_page.get_season_and_episode_number()
        assert (season == season_new and episode + 1 == episode_new) or (season + 1 == season_new and episode_new == 1), \
            'Episode should be {s}x{e} or {ss}x01. And we get that episode {s_}x{e_}'.format(s=season, e=episode + 1,
                                                                                             ss=season + 1,
                                                                                             s_=season_new,
                                                                                             e_=episode_new)
        general.open_statistics_steps(main_shows_page)
        new_watched_num = statistics_page.get_watched_number()
        assert watched_num + 1 == new_watched_num, 'Watched numbers does not match'
