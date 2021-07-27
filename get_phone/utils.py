import random
import string


# def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

def random_string_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_report_id_generator(instance):
    report_new_id = random_string_generator(size=8)

    Klass = instance.__class__

    qs_exists = Klass.objects.filter(report_id=report_new_id).exists()
    if qs_exists:
        return unique_report_id_generator(instance)
    return report_new_id
