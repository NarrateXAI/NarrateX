from pydantic import BaseModel
from typing import Dict, List, Optional


class Character_Lore(BaseModel):
    character_name: str
    background: Dict
    personality: Dict
    skills: Dict
    missions: Dict
    motivations: Dict
    challenges: Dict
    relationships: Dict
    planets: List


mc_lore = Character_Lore(
  character_name= "Madival Voyager",
  background= {
    "origin": "Madival was born on the Martian colony Arco Magna, a hub for interstellar research and trade.",
    "upbringing": "Raised in a family of explorers, Madival grew up surrounded by tales of cosmic discovery and lost civilizations. His mother was a renowned xenobiologist, and his father a cartographer of uncharted star systems.",
    "education": "Graduated from the Galactic Institute of Exploration with degrees in Astrophysics and Advanced AI Navigation. Specialized in deep-space survival and ancient alien linguistics."
  },
  personality= {
    "traits": [
      "Resilient under pressure",
      "Inquisitive with a hunger for knowledge",
      "Witty and resourceful in dire situations",
      "Compassionate yet pragmatic"
    ],
    "flaws": [
      "Often overanalyzes decisions",
      "Struggles to delegate responsibility"
    ]
  },
  skills= {
    "technical": [
      "Mastery in spacecraft engineering and repair",
      "Expertise in decoding alien languages and symbols",
      "Proficient in using adaptive AI systems for exploration"
    ],
    "soft_skills": [
      "Skilled negotiator in tense situations",
      "Instinctive leader with a knack for building morale"
    ]
  },
  equipment= {
    "signature_gear": [
      "Quantum Field Scanner: A device capable of analyzing unknown environments in real time.",
      "Chrono-Gauntlet: A wrist-mounted tool allowing limited manipulation of time for brief moments.",
      "Xenon Blade: A compact, plasma-based tool for cutting and self-defense."
    ]
  },
  missions= {
    "primary_goal": "To uncover the secrets of the Eidolon Nexus, a planet shrouded in iridescent fog and said to hold the key to humanity’s survival.",
    "notable_expeditions": [
      {
        "name": "The Luminara Prime Twilight Trek",
        "outcome": "Discovered bioluminescent flora capable of producing limitless clean energy."
      },
      {
        "name": "Kryonix Delta Ice Ruin Expedition",
        "outcome": "Unearthed artifacts hinting at an ancient civilization with advanced technology."
      },
      {
        "name": "Zephyros Vortex Storm Navigation",
        "outcome": "First human to decode the 'sound storms,' revealing navigational data for distant galaxies."
      }
    ]
  },
  motivations= {
    "personal": "Driven by the legacy of his explorer parents, Madival seeks to etch his own name into the stars.",
    "philosophical": "Believes humanity's future lies in understanding and harmonizing with the mysteries of the universe."
  },
  challenges= {
    "external": [
      "Hostile alien species and rival factions vying for interstellar dominance.",
      "Treacherous planetary conditions and unpredictable cosmic phenomena."
    ],
    "internal": [
      "Struggles with self-doubt when facing seemingly insurmountable odds.",
      "A lingering sense of guilt from a failed mission that cost the lives of several crew members."
    ]
  },
  relationships= {
    "allies": [
      {
        "name": "Dr. Aria Solara",
        "role": "Alien linguist and trusted confidant",
        "connection": "Childhood friend and expedition partner"
      },
      {
        "name": "R3-VOK",
        "role": "AI companion",
        "connection": "Advanced AI system that serves as his navigator and moral sounding board"
      }
    ],
    "adversaries": [
      {
        "name": "Vexar Syndicate",
        "role": "Intergalactic crime organization",
        "conflict": "Seeks to exploit the Eidolon Nexus for their gain, putting them at odds with Madival."
      }
    ]
  },
  planets= [
    {
      "name": "Arco Magna",
      "type": "Martian Colony",
      "description": "A sprawling research and trade hub on Mars, known for its pioneering advancements in interstellar exploration.",
      "unique_features": [
        "First human colony on Mars to develop terraforming domes with artificial gravity.",
        "Home to the Galactic Institute of Exploration, a renowned center for astrophysics and xenobiology."
      ],
      "challenges": [
        "Harsh Martian environment outside protective domes.",
        "Frequent political disputes over resource distribution and colony expansion."
      ],
      "relation_to_madival": "Madival Voyager’s birthplace and the foundation of his passion for exploration, inspired by his parents' work as interstellar researchers."
    },
    {
      "name": "Zephyros Vortex",
      "type": "Gas Giant",
      "description": "A swirling, multicolored stormy planet with floating crystalline platforms.",
      "unique_features": [
        "Constant electrical discharges create a visually stunning atmosphere.",
        "Atmosphere generates 'sound storms,' carrying mysterious messages."
      ],
      "challenges": [
        "Extreme winds disrupt navigation.",
        "Electromagnetic interference hampers communication."
      ]
    },
    {
      "name": "Luminara Prime",
      "type": "Tidally Locked Terrestrial Planet",
      "description": "A world divided into perpetual daylight, eternal darkness, and a habitable twilight zone.",
      "unique_features": [
        "Bioluminescent plants in the dark side produce clean energy.",
        "Spore emissions alter time perception for nearby life forms."
      ],
      "challenges": [
        "Surviving extreme heat and cold.",
        "Avoiding overexposure to time-distorting spores."
      ]
    },
    {
      "name": "Kryonix Delta",
      "type": "Frozen World",
      "description": "A planet of icy plains, towering glaciers, and ancient buried ruins.",
      "unique_features": [
        "Auroras and reflective ice create dazzling, disorienting visuals.",
        "Buried ruins contain artifacts with unknown powers."
      ],
      "challenges": [
        "Navigating subzero temperatures.",
        "Dealing with sudden terrain shifts due to geothermal activity."
      ]
    },
    {
      "name": "Aurumis IV",
      "type": "Desert Planet",
      "description": "A shimmering golden desert with hidden underground oases.",
      "unique_features": [
        "Golden sands contain a mineral that disrupts electronics but can be refined into a potent energy source.",
        "Twin suns create stunning mirages."
      ],
      "challenges": [
        "Frequent and intense sandstorms.",
        "Scarcity of water and competition for resources."
      ]
    },
    {
      "name": "Eidolon Nexus",
      "type": "Mysterious Planet",
      "description": "A planet shrouded in iridescent fog with floating structures defying physics.",
      "unique_features": [
        "Fog contains microorganisms inducing shared hallucinations.",
        "Floating structures hint at advanced alien technology or magic."
      ],
      "challenges": [
        "Determining reality amidst illusions.",
        "Avoiding psychological effects of prolonged fog exposure."
      ]
    }
  ]
)