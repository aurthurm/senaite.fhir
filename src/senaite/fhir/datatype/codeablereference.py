# -*- coding: utf-8 -*-
from senaite.fhir.datatype.codeableconcept import CodeableConcept
from senaite.fhir.datatype.coding import Coding


class CodeableReference(dict):
    """A common pattern in healthcare records is that a single element may
    refer to either a concept in principle, or a specific instance of the
    concept as seen in practice. For instance, a medication may be prescribed
    because the patient has a headache - e.g. to refer to a headache by a
    SNOMED CT code for a kind of headache. Alternatively, the record may refer
    to a specific observation or problem in the problem list as evidence for
    the patient's headache, which conveys details specific to the patient.
    This is a particular example of a more general pattern; e.g. it also
    applies to locations (something happened 'in a hospital', vs something
    happened in a particular identified hospital).

    The CodeableReference datatype represents this pattern, and may be bound to
    a value set to allow for a conceptual representation. In such cases, the
    value set binding actually applies to the concept element as it usually
    would for a CodeableConcept. Alternatively, the CodeableReference datatype
    can refer to another resource, and the list of valid target types for the
    CodeableReference resource applies to the Reference as described above.

    In principle, this datatype allows for either a reference or a concept, or
    both. If both are present, they are expected to be consistent with each
    other - e.g. the concept is to a code for headache, and the resource
    reference describes a headache. Note that it is not generally computably
    proveable whether this is true or not.

    The targetProfile and binding constraints on the CodeableReference apply to
    the CodeableReference.reference or the CodeableReference.concept
    respectively as appropriate and they SHALL NOT be specified directly on the
    .reference or .concept elements.

    This datatype can be constrained in profiles so that only concept or
    reference are allowed, and profiles can restrict the bound value sets
    and allowed target resource types.

    This datatype is mostly used for reason for an action.

    https://hl7.org/fhir/R5/references.html#CodeableReference
    """

    @property
    def concept(self):
        """A reference to a concept - e.g. the information is identified by its
        general class to the degree of precision found in the terminology.
        https://hl7.org/fhir/R5/references-definitions.html#CodeableReference.concept
        """
        data = self.get("concept")
        return CodeableConcept(data) if data else None
