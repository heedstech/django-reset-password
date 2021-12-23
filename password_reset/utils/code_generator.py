import random
import string
import hashlib

from ..models import RecoveryCode


def generate_code(user, size=6, letters=True, numbers=True, attempt=0):

    attempt += 1

    if attempt > 3:
        raise ValueError('Recovery code could not be generated')

    if attempt == 0:
        if (size < 4 or size > 12):
            raise ValueError('Size must be between 4 and 12')

        if (not letters and not numbers):
            raise ValueError('Must choose at least one character option')

    first_half = int(size / 2)
    second_half = size - first_half

    code = ''

    if numbers:
        if letters:
            code = ''.join(random.choice(string.ascii_uppercase)
                           for x in range(first_half))
            code += ''.join(random.choice(string.digits)
                            for x in range(second_half))
        else:
            code = ''.join(random.choice(string.digits) for x in range(size))
    else:
        code = ''.join(random.choice(string.ascii_uppercase)
                       for x in range(size))

    l = list(code)
    random.shuffle(l)
    code = ''.join(l)

    hash_code = hashlib.sha256((
        user.email +
        user.password +
        code
    ).encode('utf-8')).hexdigest().upper()

    try:
        # RecoveryCode.objects.create(user=user, hash_code=hash_code)
        recovey = RecoveryCode(user=user, hash_code=hash_code)
        recovey.save()
        # print(recovey.)
    except Exception as e:
        print(e)
        code = generate_code(user, attempt=attempt)

    return code
