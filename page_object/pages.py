import pytest
from appium.webdriver.common.touch_action import TouchAction


class BaseDriver:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(15)
        self.action = TouchAction(self.driver)


class AddShow(BaseDriver):
    @pytest.allure.step('Search through list of shows on adding show page')
    def search_through_list(self):
        shows = self.driver.find_elements_by_id('textViewAddTitle')
        self.action.long_press(shows[-1]).move_to(shows[0]).release().perform()

    @pytest.allure.step('Tap on random show')
    def tap_on_selected_show(self):
        shows = self.driver.find_elements_by_id('textViewAddTitle')
        show_name = shows[1].get_attribute('text')
        self.action.tap(shows[1]).perform()
        return show_name, ShowWidget(self.driver)


class ShowWidget(BaseDriver):
    @pytest.allure.step('Tap on AddShow button on show widget')
    def add_show(self, show_name):
        dialog_name = self.driver.find_element_by_id('textViewAddTitle')
        if show_name in dialog_name.get_attribute('text'):
            el1 = self.driver.find_element_by_id('buttonPositive')
            self.action.tap(el1).perform()
            return AddShow(self.driver)
        else:
            raise Exception('Show names does not match on dialog screen')


class MainShowsPage(BaseDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.top_layout = TopLayout(driver)
        self.func_buttons = FunctionalButtons(driver)

    @pytest.allure.step('Tap on floating plus')
    def tap_on_floating_plus(self):
        el = self.driver.find_element_by_id('buttonShowsAdd')
        self.action.tap(el).perform()
        return AddShow(self.driver)

    @pytest.allure.step('Get show name on the main screen')
    def get_show_from_main_screen(self):
        series_name = self.driver.find_element_by_id('seriesname')
        return series_name

    @pytest.allure.step('Get season and episode number from the main screen')
    def get_season_and_episode_number(self):
        episode_name = self.driver.find_element_by_id('TextViewShowListNextEpisode')
        text = episode_name.get_attribute('text')
        words = text.split()
        numbers = words[0].split('x')
        season, episode = (int(y) for y in numbers)
        return season, episode

    @pytest.allure.step('Tap on the show on the main screen')
    def tap_on_show(self):
        episode_name = self.driver.find_element_by_id('TextViewShowListNextEpisode')
        self.action.tap(episode_name).perform()
        return EpisodePage(self.driver)


class EpisodePage(BaseDriver):
    @pytest.allure.step('Set curretn episode watched')
    def set_episode_watched(self):
        check_mark = self.driver.find_element_by_id('buttonEpisodeWatched')
        self.action.tap(check_mark).perform()


class TopLayout(BaseDriver):
    @pytest.allure.step('Open menu bar from the top layout')
    def open_menu_bar(self):
        toolbar = self.driver.find_element_by_id('sgToolbar')
        menu = toolbar.find_element_by_class_name('android.widget.ImageButton')
        self.action.tap(menu).perform()
        return MenuBar(self.driver)

    @pytest.allure.step('Open main shows page from the top layout')
    def open_main_show_page(self):
        switch_to_shows = self.driver.find_element_by_id('textViewTabStripItem')
        self.action.tap(switch_to_shows).perform()


class FunctionalButtons(BaseDriver):
    @pytest.allure.step('Press back button')
    def press_back_button(self):
        """
        4 - back button key code.
        For more information follow the link
        https://developer.android.com/reference/android/view/KeyEvent.html#KEYCODE_BACK
        """
        self.driver.press_keycode(4)


class MenuBar(BaseDriver):
    @pytest.allure.step('Tap on statistics item in menu bar')
    def tap_on_statistics(self):
        items = self.driver.find_elements_by_id('design_menu_item_text')
        for item in items:
            if item.get_attribute('text') == 'Statistics':
                self.action.tap(item).perform()
                return StatisticsPage(self.driver)


class StatisticsPage(BaseDriver):
    @pytest.allure.step('Get number of added shows from statistic page')
    def get_number_of_shows(self):
        number = int(self.driver.find_element_by_id('textViewStatsShows').get_attribute('text'))
        return number

    @pytest.allure.step('Get number of watched episodes from statistic page')
    def get_watched_number(self):
        stats = self.driver.find_element_by_id('textViewStatsEpisodesWatched')
        text = stats.get_attribute('text')
        watched_num = int(text.split()[0])
        return watched_num
