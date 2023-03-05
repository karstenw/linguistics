"""
Constants and literals used in wordnets.
"""


SENSE_RELATIONS = frozenset([
    'antonym',
    'also',
    'participle',
    'pertainym',
    'derivation',
    'domain_topic',
    'has_domain_topic',
    'domain_region',
    'has_domain_region',
    'exemplifies',
    'is_exemplified_by',
    'similar',
    'other',
    'feminine',
    'has_feminine',
    'masculine',
    'has_masculine',
    'young',
    'has_young',
    'diminutive',
    'has_diminutive',
    'augmentative',
    'has_augmentative',
    'anto_gradable',
    'anto_simple',
    'anto_converse',
    'simple_aspect_ip',
    'secondary_aspect_ip',
    'simple_aspect_pi',
    'secondary_aspect_pi',
])

SENSE_SYNSET_RELATIONS = frozenset([
    'other',
    'domain_topic',
    'domain_region',
    'exemplifies',
])

SYNSET_RELATIONS = frozenset([
    'agent',
    'also',
    'attribute',
    'be_in_state',
    'causes',
    'classified_by',
    'classifies',
    'co_agent_instrument',
    'co_agent_patient',
    'co_agent_result',
    'co_instrument_agent',
    'co_instrument_patient',
    'co_instrument_result',
    'co_patient_agent',
    'co_patient_instrument',
    'co_result_agent',
    'co_result_instrument',
    'co_role',
    'direction',
    'domain_region',
    'domain_topic',
    'exemplifies',
    'entails',
    'eq_synonym',
    'has_domain_region',
    'has_domain_topic',
    'is_exemplified_by',
    'holo_location',
    'holo_member',
    'holo_part',
    'holo_portion',
    'holo_substance',
    'holonym',
    'hypernym',
    'hyponym',
    'in_manner',
    'instance_hypernym',
    'instance_hyponym',
    'instrument',
    'involved',
    'involved_agent',
    'involved_direction',
    'involved_instrument',
    'involved_location',
    'involved_patient',
    'involved_result',
    'involved_source_direction',
    'involved_target_direction',
    'is_caused_by',
    'is_entailed_by',
    'location',
    'manner_of',
    'mero_location',
    'mero_member',
    'mero_part',
    'mero_portion',
    'mero_substance',
    'meronym',
    'similar',
    'other',
    'patient',
    'restricted_by',
    'restricts',
    'result',
    'role',
    'source_direction',
    'state_of',
    'target_direction',
    'subevent',
    'is_subevent_of',
    'antonym',
    'feminine',
    'has_feminine',
    'masculine',
    'has_masculine',
    'young',
    'has_young',
    'diminutive',
    'has_diminutive',
    'augmentative',
    'has_augmentative',
    'anto_gradable',
    'anto_simple',
    'anto_converse',
    'ir_synonym',
])


REVERSE_RELATIONS = {
    'hypernym': 'hyponym',
    'hyponym': 'hypernym',
    'instance_hypernym': 'instance_hyponym',
    'instance_hyponym': 'instance_hypernym',
    'antonym': 'antonym',
    'eq_synonym': 'eq_synonym',
    'similar': 'similar',
    'meronym': 'holonym',
    'holonym': 'meronym',
    'mero_location': 'holo_location',
    'holo_location': 'mero_location',
    'mero_member': 'holo_member',
    'holo_member': 'mero_member',
    'mero_part': 'holo_part',
    'holo_part': 'mero_part',
    'mero_portion': 'holo_portion',
    'holo_portion': 'mero_portion',
    'mero_substance': 'holo_substance',
    'holo_substance': 'mero_substance',
    'also': 'also',
    'state_of': 'be_in_state',
    'be_in_state': 'state_of',
    'causes': 'is_caused_by',
    'is_caused_by': 'causes',
    'subevent': 'is_subevent_of',
    'is_subevent_of': 'subevent',
    'manner_of': 'in_manner',
    'in_manner': 'manner_of',
    'attribute': 'attribute',
    'restricts': 'restricted_by',
    'restricted_by': 'restricts',
    'classifies': 'classified_by',
    'classified_by': 'classifies',
    'entails': 'is_entailed_by',
    'is_entailed_by': 'entails',
    'domain_topic': 'has_domain_topic',
    'has_domain_topic': 'domain_topic',
    'domain_region': 'has_domain_region',
    'has_domain_region': 'domain_region',
    'exemplifies': 'is_exemplified_by',
    'is_exemplified_by': 'exemplifies',
    'role': 'involved',
    'involved': 'role',
    'agent': 'involved_agent',
    'involved_agent': 'agent',
    'patient': 'involved_patient',
    'involved_patient': 'patient',
    'result': 'involved_result',
    'involved_result': 'result',
    'instrument': 'involved_instrument',
    'involved_instrument': 'instrument',
    'location': 'involved_location',
    'involved_location': 'location',
    'direction': 'involved_direction',
    'involved_direction': 'direction',
    'target_direction': 'involved_target_direction',
    'involved_target_direction': 'target_direction',
    'source_direction': 'involved_source_direction',
    'involved_source_direction': 'source_direction',
    'co_role': 'co_role',
    'co_agent_patient': 'co_patient_agent',
    'co_patient_agent': 'co_agent_patient',
    'co_agent_instrument': 'co_instrument_agent',
    'co_instrument_agent': 'co_agent_instrument',
    'co_agent_result': 'co_result_agent',
    'co_result_agent': 'co_agent_result',
    'co_patient_instrument': 'co_instrument_patient',
    'co_instrument_patient': 'co_patient_instrument',
    'co_result_instrument': 'co_instrument_result',
    'co_instrument_result': 'co_result_instrument',
    'pertainym': 'pertainym',
    'derivation': 'derivation',
    'simple_aspect_ip': 'simple_aspect_pi',
    'simple_aspect_pi': 'simple_aspect_ip',
    'secondary_aspect_ip': 'secondary_aspect_pi',
    'secondary_aspect_pi': 'secondary_aspect_ip',
    'feminine': 'has_feminine',
    'has_feminine': 'feminine',
    'masculine': 'has_masculine',
    'has_masculine': 'masculine',
    'young': 'has_young',
    'has_young': 'young',
    'diminutive': 'has_diminutive',
    'has_diminutive': 'diminutive',
    'augmentative': 'has_augmentative',
    'has_augmentative': 'augmentative',
    'anto_gradable': 'anto_gradable',
    'anto_simple': 'anto_simple',
    'anto_converse': 'anto_converse',
    'ir_synonym': 'ir_synonym',
    # 'participle': '',
    # 'other': '',
}

# Adjective Positions

ADJPOSITIONS = frozenset((
    'a',   # attributive
    'ip',  # immediate postnominal
    'p',   # predicative
))


# Parts of Speech

NOUN = 'n'  #:
VERB = 'v'  #:
ADJ = ADJECTIVE = 'a'  #:
ADV = ADVERB = 'r'  #:
ADJ_SAT = ADJECTIVE_SATELLITE = 's'  #:
PHRASE = 't'  #:
CONJ = CONJUNCTION = 'c'  #:
ADP = ADPOSITION = 'p'  #:
OTHER = 'x'  #:
UNKNOWN = 'u'  #:

PARTS_OF_SPEECH = frozenset((
    NOUN,
    VERB,
    ADJECTIVE,
    ADVERB,
    ADJECTIVE_SATELLITE,
    PHRASE,
    CONJUNCTION,
    ADPOSITION,
    OTHER,
    UNKNOWN,
))


# Lexicographer Files
# from https://wordnet.princeton.edu/documentation/lexnames5wn

LEXICOGRAPHER_FILES = {
    'adj.all': 0,
    'adj.pert': 1,
    'adv.all': 2,
    'noun.Tops': 3,
    'noun.act': 4,
    'noun.animal': 5,
    'noun.artifact': 6,
    'noun.attribute': 7,
    'noun.body': 8,
    'noun.cognition': 9,
    'noun.communication': 10,
    'noun.event': 11,
    'noun.feeling': 12,
    'noun.food': 13,
    'noun.group': 14,
    'noun.location': 15,
    'noun.motive': 16,
    'noun.object': 17,
    'noun.person': 18,
    'noun.phenomenon': 19,
    'noun.plant': 20,
    'noun.possession': 21,
    'noun.process': 22,
    'noun.quantity': 23,
    'noun.relation': 24,
    'noun.shape': 25,
    'noun.state': 26,
    'noun.substance': 27,
    'noun.time': 28,
    'verb.body': 29,
    'verb.change': 30,
    'verb.cognition': 31,
    'verb.communication': 32,
    'verb.competition': 33,
    'verb.consumption': 34,
    'verb.contact': 35,
    'verb.creation': 36,
    'verb.emotion': 37,
    'verb.motion': 38,
    'verb.perception': 39,
    'verb.possession': 40,
    'verb.social': 41,
    'verb.stative': 42,
    'verb.weather': 43,
    'adj.ppl': 44,
}

# resource types

_WORDNET = 'wordnet'
_ILI = 'ili'