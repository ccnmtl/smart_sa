from lettuce import world, step

@step('there is an assessmentquiz')
def there_is_an_assessmentquiz(self):
    if not world.using_selenium:
        assert len(world.dom.cssselect('#assessmentquiz')) > 0
    else:
        assert world.firefox.find_element_by_id('assessmentquiz')

@step('I fill in all (\d)s in the quiz')
def fill_in_quiz(self,value):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    for i in world.firefox.find_elements_by_tag_name('input'):
        if i.get_attribute('type') == 'radio' and i.get_attribute('value') == value:
            i.click()
