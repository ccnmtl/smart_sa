from lettuce import world, step
import time

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
            
@step('I answer (\d) for question ([0-9][0-9]?)')
def i_fill_in_value_for_question_number(step, value, number):
    name = "q%s" % number
    elts = world.firefox.find_elements_by_name(name)
    for i in elts:
        if i.get_attribute('type') == 'radio' and i.get_attribute('value') == value:
            i.click()
            
@step(u"Then I'm asked to answer all the questions")
def then_i_m_asked_to_enter_all_the_questions(step):
    alert = world.firefox.switch_to_alert()
    assert alert.text.startswith("Please answer all the questions"), "Alert text valid"
    alert.accept()
    
def verify_score(text):   
    score = world.firefox.find_element_by_css_selector("li.inrange")
    
    found = False
    try:
        headline = score.find_element_by_css_selector("div.headline")
        if headline: 
            found = headline.text.find(text) >= 0
    except:
        pass
    
    if not found:
        try:
            script = score.find_element_by_css_selector("div.script")
            if script:
                found = script.text.find(text) >= 0
        except:
            pass
    
    return found

@step(u'Then my score says "([^"]*)"')
def then_my_score_says_text(step, text):
    found = False
    try:
        found = verify_score(text)
    except:
        time.sleep(2)
        found = verify_score(text)
        
    if not found:
        assert False, "[%s] not found in score headline or script" % (text)    
    
            
