from marvin import ai_fn
from raw_data import test_data

# good example here: https://github.com/jacopotagliabue/foundation-models-for-dbt-entity-matching/blob/main/src/marvin-duck/marvin_entity_resolution.py


short_test_data = """I want help skipping tasks in a flow run. How can I accomplish this?"""

@ai_fn
def classify_support_thread(support_thread: str) -> bool:
    """ 
    Return True if this support thread reporting a bug, return False if this support thread is requesting a feature?
    """

if __name__ == "__main__":

    short_test_data = classify_support_thread(support_thread=short_test_data)
    print(short_test_data)

    print('---')

    tech_question = classify_support_thread(support_thread=test_data.tech_question)
    print(tech_question)

    print('---')

    feature_request = classify_support_thread(support_thread=test_data.feature_request)
    print(feature_request)