# Support for basic modular math in ElectionGuard. This code's primary purpose is to be "correct",
# in the sense that performance may be less than hand-optimized C code, and no guarantees are
# made about timing or other side-channels.

from typing import Final, Union, NamedTuple

# Constants used by ElectionGuard
Q: Final[int] = pow(2, 256) - 189
P: Final[int] = pow(2, 4096) - 69 * Q - 2650872664557734482243044168410288960
R: Final[int] = ((P - 1) * pow(Q, -1, P)) % P
G: Final[int] = pow(2, R, P)
G_INV: Final[int] = pow(G, -1, P)


class ElementModQ(NamedTuple):
    """An element of the smaller `mod q` space, i.e., in [0, Q), where Q is a 256-bit prime."""
    elem: int


ZERO_MOD_Q: Final[ElementModQ] = ElementModQ(0)
ONE_MOD_Q: Final[ElementModQ] = ElementModQ(1)


class ElementModP(NamedTuple):
    """An element of the larger `mod p` space, i.e., in [0, P), where P is a 4096-bit prime."""
    elem: int


ZERO_MOD_P: Final[ElementModP] = ElementModP(0)
ONE_MOD_P: Final[ElementModP] = ElementModP(1)

ElementModPOrQ = Union[ElementModP, ElementModQ]  # generally useful typedef


def mult_inv_p(e: ElementModPOrQ) -> ElementModP:
    """
    Computes the multiplicative inverse mod p.
    :param e:  An element in [1, P).
    """
    if e.elem == 0:
        raise Exception("No multiplicative inverse for zero")
    return ElementModP(pow(e.elem, -1, P))


def pow_mod_p(b: ElementModPOrQ, e: ElementModPOrQ) -> ElementModP:
    """
    Computes b^e mod p.
    :param b: An element in [0,P).
    :param e: An element in [0,P).
    """
    return ElementModP(pow(b.elem, e.elem, P))


def mult_mod_p(a: ElementModPOrQ, b: ElementModPOrQ) -> ElementModP:
    """
    Computes a * b mod p.
    :param a: An element in [0,P).
    :param b: An element in [0,P).
    """
    return ElementModP((a.elem * b.elem) % P)


def g_pow(e: ElementModPOrQ) -> ElementModP:
    """
    Computes g^e mod p.
    :param e: An element in [0,P).
    """
    return pow_mod_p(ElementModP(G), e)


def validate_p(p: ElementModP) -> None:
    """
    Validates that the element is actually within the bounds of [0,P). Raises an `Exception` if it's not.
    """
    if p.elem < 0 or p.elem >= P:
        raise Exception("element out of mod-p range!")


def validate_q(q: ElementModQ) -> None:
    """
    Validates that the element is actually within the bounds of [0,Q). Raises an `Exception` if it's not.
    """
    if q.elem < 0 or q.elem >= Q:
        raise Exception("element out of mod-q range!")


def validate_p_no_zero(p: ElementModP) -> None:
    """
    Validates that the element is actually within the bounds of [1,P). Raises an `Exception` if it's not.
    """
    if p.elem <= 0 or p.elem >= P:
        raise Exception("element out of mod-p range!")


def validate_q_no_zero(q: ElementModQ) -> None:
    """
    Validates that the element is actually within the bounds of [1,Q). Raises an `Exception` if it's not.
    """
    if q.elem <= 0 or q.elem >= Q:
        raise Exception("element out of mod-q range!")
