# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

"""

Objet atome.

---------
Arguments

valeur
    :Atome
        Léve une erreur
    :Ion
        Transforme l'ion en atome.
    :int
        Equivaut au nombre de proton et créer un Atome.

neutron
    :int
        Définie le nombre de proton pour l'isotope.

------
Retour

Atome
    .element:str
    .symbole:str
    .categorie:str

    .proton:int
    .neutron:int
    .electron:int
    .nucleon:int

    .masse:float
    .masse_atomique_relative:float

    .configuration:list
    .couches:list

    .notation()
    .notation_symbole()
    .notation_couche()
    .notation_configuration()
"""


from typing import Union, Any, Optional


from . import base
from .base import (
    Atome, Molecule,
    Ion, IonMonoAtomique, IonPolyAtomique,
    Electron, Proton, Neutron
)
from .. import utile
from .. import exception
from .. import objets


class Atome:
    """
    ### &doc_id atome:class
    """

    __slots__ = (
        'element', 'symbole', 'categorie',
        'proton', 'neutron', 'nucleon', 'electron', 
        'masse', 'masse_atomique_relative', 
        'configuration', 'couches'
    )

    def __init__(self, 
            valeur:Union[int, str, IonMonoAtomique],
            neutron:Optional[int] = None
        ) -> None:
        """
        ### &doc_id atome:init
        """

        self.neutron = neutron

        utile.get_info(self, valeur)

        self.electron = self.proton

        if self.neutron is None:
            self.neutron = round(self.masse_atomique_relative) - self.proton

        self.masse = utile.get_masse(self)

        self.nucleon = self.proton + self.neutron

        self.configuration = utile.configuration_electronique(self)

    def __add__(self, 
            obj: Union[Proton, Neutron, Electron, Atome]
        ) -> Union[Atome, Molecule, IonMonoAtomique]:

        if isinstance(obj, objets.Proton):
            return Atome(self.proton + obj.valeur)

        elif isinstance(obj, objets.Neutron):
            return Atome(self.proton, self.neutron + obj.valeur)

        elif isinstance(obj, objets.Electron):
            return IonMonoAtomique(self.proton, self.electron + obj.valeur)

        elif isinstance(obj, objets.Atome):
            return Molecule([self, obj])

        else:
            raise exception.Incompatible(self, obj)

    def __iadd__(self, 
            obj: Union[Proton, Neutron, Electron, Atome]
        ) -> Union[Atome, Molecule, IonMonoAtomique]:
        return self + obj

    def __sub__(self, 
            obj: Union[Proton, Neutron, Electron]
        ) -> Union[Atome, IonMonoAtomique]:

        if isinstance(obj, objets.Proton):
            return Atome(self.proton - obj.valeur)

        elif isinstance(obj, objets.Neutron):
            return Atome(self.proton, self.neutron - obj.valeur)

        elif isinstance(obj, objets.Electron):
            return IonMonoAtomique(self.proton, self.electron - obj.valeur)

        else:
            raise exception.Incompatible(self, obj)

    def __isub__(self, 
            obj: Union[Proton, Neutron, Electron]
        ) -> Union[Atome, IonMonoAtomique]:
        return self - obj

    def __mul__(self, obj: int) -> Molecule:
        return Molecule([self] * obj)

    def __str__(self) -> str:
        str__ = (
            "Atome %s" % self.notation()
            + (
                "\n Elément: %s" % self.element[utile.params.langue] 
                if utile.params.element else ''
            )
            + (
                "\n Catégorie: %s" % self.categorie[utile.params.langue] 
                if utile.params.categorie else ''
            )
            + (
                "\n Proton(s): %s" % self.proton 
                if utile.params.proton else ''
            )
            + (
                "\n Neutron(s): %s" % self.neutron 
                if utile.params.neutron else ''
            )
            + (
                "\n Electron(s): %s" % self.electron 
                if utile.params.electron else ''
            )
            + (
                "\n Masse: %s" % self.masse 
                if utile.params.masse else ''
            )
            + (
                "\n Masse atomique relative: %s" 
                % self.masse_atomique_relative
                if utile.params.masse_relative else ''
            )
            + (
                "\n Couche électronique: %s" % self.notation_couche() 
                if utile.params.couches else ''
            )
            + (
                "\n Configuration électronique: %s" 
                % self.notation_configuration()
                if utile.params.configuration else ''
            )
        )

        return (
            str__ if not utile.params.calculatrice
            else
                str__.replace('è', 'e').replace('é', 'e')
        )

    def __repr__(self) -> str:
        return self.notation_symbole()

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def notation(self) -> str:
        """
        ### &doc_id atome:notation
        """
        return "%s Z=%s A=%s" % (
            self.symbole, self.proton, self.proton + self.neutron
        )

    def notation_symbole(self, A:bool = True, Z:bool = True) -> str:
        """
        ### &doc_id atome:notation_symbole
        """

        return "%s%s%s" % (
            '' if not A or utile.params.calculatrice
            else
                ''.join(
                    utile.exposants[int(num)] 
                    for num in str(self.proton + self.neutron)
                )
            ,
            '' if not Z or utile.params.calculatrice
            else
                ''.join(
                    utile.sous_exposants[int(num)] 
                    for num in str(self.proton)
                )
            ,
            self.symbole
        )

    
    notation_couche = utile.notation_couche

    notation_configuration = utile.notation_configuration


base.Atome = Atome