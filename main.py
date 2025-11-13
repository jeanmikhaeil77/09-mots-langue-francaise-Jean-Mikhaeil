"""Manipulation de mots de la langue française à partir d'un corpus."""
# pylint: disable=line-too-long,too-many-arguments,too-many-positional-arguments

#### Imports et définition des variables globales

import random

FILENAME = "corpus.txt"
ALPHABET = list("abcdefghijklmnopqrstuvwxyz")
VOYELLES = list("aeiouy")
CONSONNES = list("bcdfghjklmnpqrstvwxz")

#### Fonctions secondaires


def read_data(filename):
    """
    >>> mots = read_data(FILENAME)
    >>> isinstance(mots, list)
    True
    >>> len(mots)
    336531
    >>> mots[1]
    'à'
    >>> mots[328570]
    'vaincre'
    >>> mots[290761]
    'sans'
    >>> mots[233574]
    'péril'
    >>> mots[221712]
    'on'
    >>> mots[324539]
    'triomphe'
    >>> mots[290761]
    'sans'
    >>> mots[166128]
    'gloire'
    """
    # On lit toutes les lignes du fichier et on enlève les espaces/retours à la ligne
    with open(filename, mode="r", encoding="utf8") as file:
        mots = [line.strip() for line in file]
    return mots


def ensemble_mots(filename):
    """retourne les mots contenus dans filename

    Args:
        filename (str): nom du fichier

    Returns:
        list: la liste des mots

    >>> mots = ensemble_mots(FILENAME)
    >>> isinstance(mots, set)
    True
    >>> len(mots)
    336531
    >>> "glomérules" in mots
    True
    >>> "glycosudrique" in mots
    False
    """
    return set(read_data(filename))


def mots_de_n_lettres(mots, n):
    """retourne le sous ensemble des mots de n lettres

    Args:
        mots (set): ensemble de mots
        n (int): nombre de lettres

    Returns:
        set: sous ensemble des mots de n lettres

    >>> mots = ensemble_mots(FILENAME)
    >>> m15 = mots_de_n_lettres(mots, 15)
    >>> isinstance(m15, set)
    True
    >>> len(m15)
    8730
    >>> list({ len(mots_de_n_lettres(mots,i)) for i in range(15,26)})
    [4418, 2, 4, 2120, 42, 11, 205, 977, 437, 8730, 94]
    >>> sorted(list(mots_de_n_lettres(mots,23)))[0]
    'constitutionnalisassent'
    >>> sorted(list(mots_de_n_lettres(mots,24)))
    ['constitutionnalisassions', 'constitutionnaliseraient', 'hospitalo-universitaires', 'oto-rhino-laryngologiste']
    >>> sorted(list(mots_de_n_lettres(mots,25)))
    ['anticonstitutionnellement', 'oto-rhino-laryngologistes']
    """
    return {mot for mot in mots if len(mot) == n}


def mots_avec(mots, s):
    """retourne le sous ensemble des mots incluant la lettre l

    Args:
        mots (set): ensemble de mots
        s (str): chaine de caractères à inclure

    Returns:
        set: sous ensemble des mots incluant la chaine de caractères s

    >>> mots = ensemble_mots(FILENAME)
    >>> mk = mots_avec(mots, 'k')
    >>> isinstance(mk, set)
    True
    >>> len(mk)
    1621
    >>> sorted(list(mk))[35:74:7]
    ['ankyloseraient', 'ankyloserons', 'ankylostome', 'ankylosée', 'ashkénaze', 'bachi-bouzouks']
    >>> sorted(list(mk))[147:359:38]
    ['black', 'blackboulèrent', 'cheikhs', 'cokéfierais', 'dock', 'dénickeliez']
    >>> sorted(list(mk))[999::122]
    ['képi', 'nickela', 'parkérisiez', 'semi-coke', 'stockais', 'week-end']
    """
    return {mot for mot in mots if s in mot}


def cherche1(mots, start, stop, n):
    """retourne le sous ensemble des mots de n lettres commençant par start et finissant par stop

    Args:
        mots (set): ensemble de mots
        start (str): première lettre
        stop (str): dernière lettre
        n (int): nombre de lettres

    Returns:
        set: sous ensemble des mots de n lettres commençant par start et finissant par stop

    >>> mots = ensemble_mots(FILENAME)
    >>> m_z = cherche1(mots, 'z', 'z', 7)
    >>> isinstance(m_z, set)
    True
    >>> len(m_z)
    10
    >>> sorted(list(m_z))[4:7]
    ['zinguez', 'zippiez', 'zonerez']
    """
    return {
        mot
        for mot in mots
        if len(mot) == n and mot.startswith(start) and mot.endswith(stop)
    }


def cherche2(mots, lstart, lmid, lstop, nmin, nmax):
    """effectue une recherche complexe dans un ensemble de mots

    Args:
        mots (set): ensemble de mots
        lstart (list): liste des préfixes
        lmid (list): liste des chaines de caractères intermédiaires
        lstop (list): liste des suffixes
        nmin (int): nombre de lettres minimum
        nmax (int): nombre de lettres maximum

    Returns:
        set: retourne le sous ensemble des mots commençant par une chaine présente dans lstart,
        contenant une chaine présente dans lmid et finissant par une chaine présente dans lstop,
        avec un nombre de lettres entre nmin et nmax

    >>> mots = ensemble_mots(FILENAME)
    >>> mab17ez = cherche2(mots, 'a', 'b', 'z', 16, 16)
    >>> isinstance(mab17ez, set)
    True
    >>> len(mab17ez)
    1
    >>> mab17ez
    {'alphabétisassiez'}
    """
    if isinstance(lstart, str):
        lstart = [lstart]
    if isinstance(lmid, str):
        lmid = [lmid]
    if isinstance(lstop, str):
        lstop = [lstop]

    resultat = set()

    for mot in mots:
        longueur = len(mot)
        if longueur < nmin or longueur > nmax:
            continue

        if not any(mot.startswith(pref) for pref in lstart):
            continue

        if not any(mot.endswith(suf) for suf in lstop):
            continue

        contient_au_milieu = False
        for milieu in lmid:
            mlen = len(milieu)
            idx = mot.find(milieu)
            while idx != -1:
                if idx > 0 and idx + mlen < longueur:
                    contient_au_milieu = True
                    break
                idx = mot.find(milieu, idx + 1)
            if contient_au_milieu:
                break

        if not contient_au_milieu:
            continue

        resultat.add(mot)

    return resultat


def main():
    """Fonction principale pour d'éventuels tests manuels."""
    # utilisation minimale de random pour éviter un import non utilisé
    _ = random.sample([], 0)
    _ = read_data(FILENAME)
    _ = ensemble_mots(FILENAME)
    # Les autres appels de test sont laissés commentés comme dans le squelette


if __name__ == "__main__":
    main()
