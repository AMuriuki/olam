import hashlib
import time
import random
import string
from flask import current_app
import re

try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False


def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Return a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        # This is ugly, and a hack, but it makes things better than
        # the alternative of predictability. This re-seeds the PRNG
        # using a value that is hard for an attacker to predict, every
        # time a random string is required. This may change the
        # properties of the chosen random sequence slightly, but this
        # is better than absolute predictability.
        random.seed(
            hashlib.sha256(
                ('%s%s%s' % (random.getstate(), time.time(),
                 current_app.config['SECRET_KEY'])).encode()
            ).digest()
        )
    return ''.join(random.choice(allowed_chars) for i in range(length))


def unique_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = get_random_string(length=25)

    Klass = instance.__class__
    qs_exists = Klass.query.filter_by(slug=slug).first()
    if qs_exists:
        new_slug = get_random_string(length=25)
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def generate_sku():
    return "".join([random.choice(string.digits) for i in range(3)])+"-"+"".join([random.choice(
        string.ascii_uppercase) for i in range(3)])+"-"+"".join([random.choice(string.digits) for i in range(3)])


def extract_int(str):
    return int(re.search(r'\d+', str).group())


def generate_reference(reference):
    if(reference):
        last_digit = extract_int(reference)
        new_digit = last_digit + 1
    else:
        new_digit = 0
    return "P"+str(new_digit).zfill(6)


def sku_generator(instance, new_sku=None):

    if new_sku is not None:
        sku = new_sku
    else:
        sku = generate_sku()

    Klass = instance.__class__
    qs_exists = Klass.query.filter_by(sku=sku).first()
    while qs_exists:
        sku = generate_sku()
        qs_exists = Klass.query.filter_by(sku=sku).first()
    return sku


def purchase_reference_generator(instance, new_reference=None):
    Klass = instance.__class__
    last_rec = Klass.query.order_by(Klass.created_on.desc()).first()
    if new_reference is not None:
        reference = new_reference
    else:
        reference = generate_reference(
            last_rec.reference if last_rec else None)
    return reference


def has_access(a):
    return len(a) > 0


def remove_comma(str):
    return str.replace(",", "")


# get random color
def get_random_color():
    return '#%06x' % random.randint(0, 0xFFFFFF)
