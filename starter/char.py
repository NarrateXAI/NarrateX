from narratexai import CharacterLore, Locations

# Character Lore Template
character_lore_template = {
    "character_name": "<Character Name>",
    "identity": {
        "title_or_role": "<Character Title or Role>",
        "description": "<Brief description of the character's identity and role in the story>"
    },
    "background": {
        "origin": "<Where the character is from>",
        "key_event": "<Key event that shaped the character's life>",
        "influences": "<Cultural, personal, or environmental factors that shaped the character>"
    },
    "personality": {
        "traits": ["<Personality Trait 1>", "<Personality Trait 2>", "<Personality Trait 3>"],
        "flaws": ["<Character Flaw 1>", "<Character Flaw 2>"],
        "quirks": ["<Unique characteristic or behavior>"]
    },
    "skills": {
        "primary_skills": ["<Primary Skill 1>", "<Primary Skill 2>", "<Primary Skill 3>"],
        "secondary_skills": ["<Secondary Skill 1>", "<Secondary Skill 2>", "<Secondary Skill 3>"]
    },
    "relationships": {
        "allies": [
            {
                "name": "<Ally Name>",
                "role": "<Role or significance in the character's journey>"
            }
        ],
        "adversaries": [
            {
                "name": "<Adversary Name>",
                "description": "<Description of the adversary and their goals>"
            }
        ]
    },
    "motivations": {
        "personal_goals": "<Character's personal goals>",
        "broader_mission": "<Character's larger mission>"
    },
    "key_events": {
        "defining_moment": "<Moment that defines the character's path>",
        "current_conflict": "<The primary conflict the character is facing>"
    },
    "philosophy": {
        "beliefs": "<Character's core beliefs>",
        "outlook": "<Overall perspective on life and the universe>"
    },
    "setting_connection": {
        "environment": "<Description of the environments the character interacts with>",
        "impact": "<How the character affects the settings they visit>"
    },
    "storyline_and_missions": {
        "overall_storyline": "<Summary of the character's main story arc>",
        "missions": [
            {
                "mission_name": "<Mission Name>",
                "objective": "<Mission Objective>",
                "location": "<Mission Location>",
                "challenges": "<Key challenges faced during the mission>",
                "outcome": "<Outcome of the mission>"
            }
        ]
    },
    "locations": [
        {
            "name": "<Location Name>",
            "description": "<Description of the location>",
            "inhabitants": "<Notable inhabitants or factions>",
            "notable_features": ["<Feature 1>", "<Feature 2>", "<Feature 3>"]
        }
    ],
    "usage_notes": {
        "ideal_prompt_usage": "<Suggestions for how to use this lore in storytelling or LLM prompts>",
        "response_tone": "<Tone to use when generating responses for the character>"
    }
}

# Example usage

character_lore_kaelara = {
    "character_name": "Kaelara Sable",
    "identity": {
        "title_or_role": "The Rogue Archivist",
        "description": "Kaelara is a cunning historian and master of ancient technologies, driven by a thirst for uncovering forbidden knowledge. With a shadowy past and unmatched intellect, she walks the line between hero and outlaw."
    },
    "background": {
        "origin": "Kaelara was born in the underground city of Abyssus, hidden beneath the volcanic crust of Callidora VII.",
        "key_event": "Her family was betrayed and exiled by the Order of Eternals after her father uncovered a conspiracy involving forbidden relics.",
        "influences": "Life in exile among smugglers and archaeologists instilled in Kaelara a knack for survival and an obsession with uncovering secrets."
    },
    "personality": {
        "traits": ["Resourceful", "Charismatic", "Inquisitive"],
        "flaws": ["Reckless", "Distrustful"],
        "quirks": ["Has a habit of speaking to ancient artifacts as if they can hear her."]
    },
    "skills": {
        "primary_skills": ["Artifact analysis", "Decryption of ancient codes", "Stealth operations"],
        "secondary_skills": ["Bladed combat", "Advanced hacking", "Linguistics of extinct species"]
    },
    "relationships": {
        "allies": [
            {
                "name": "Jax Orin",
                "role": "A former smuggler and Kaelara's closest confidant, providing logistical support."
            },
            {
                "name": "Dr. Linara Thesk",
                "role": "An eccentric archaeologist who aids Kaelara with her knowledge of ancient languages."
            }
        ],
        "adversaries": [
            {
                "name": "The Order of Eternals",
                "description": "A secretive organization that seeks to control ancient relics to maintain their power."
            },
            {
                "name": "Wraith Marauders",
                "description": "A notorious band of treasure hunters often competing with Kaelara for valuable artifacts."
            }
        ]
    },
    "motivations": {
        "personal_goals": "Discover the artifact that can clear her family's name and expose the Order's corruption.",
        "broader_mission": "Prevent the Order of Eternals from using ancient relics to rewrite history and subjugate worlds."
    },
    "key_events": {
        "defining_moment": "Finding her father’s encoded journal, which hinted at a powerful relic capable of revealing the truth.",
        "current_conflict": "Recovering the ‘Heart of Callidora’ before the Order of Eternals can harness its destructive power."
    },
    "philosophy": {
        "beliefs": "Knowledge is the most dangerous and powerful weapon. It must be sought but wielded carefully.",
        "outlook": "Though often cynical, Kaelara believes some truths are worth any risk, even if it costs her everything."
    },
    "setting_connection": {
        "environment": "Kaelara explores desolate ruins, bustling black markets, and hostile alien worlds.",
        "impact": "Her discoveries often reshape the understanding of galactic history, attracting both allies and enemies."
    },
    "storyline_and_missions": {
        "overall_storyline": "Kaelara battles the Order of Eternals to uncover relics of immense power while uncovering her own family’s hidden past.",
        "missions": [
            {
                "mission_name": "The Vault of Shadows",
                "objective": "Retrieve the artifact known as the ‘Heart of Callidora.’",
                "location": "The Shadow Vault, an ancient ruin deep beneath Callidora VII’s volcanic crust.",
                "challenges": "Navigating lava fields, avoiding traps, and decoding an alien language to unlock the vault.",
                "outcome": "Kaelara retrieves the artifact but discovers the Order is already tracking her."
            }
        ]
    },
    "locations": [
        {
            "name": "Callidora VII",
            "description": "A volcanic world with massive subterranean cities and hidden ruins containing ancient technologies.",
            "inhabitants": "Exiled communities, rogue scientists, and treasure hunters.",
            "notable_features": ["Molten rivers", "Crystal caverns", "The Shadow Vault"]
        },
        {
            "name": "Abyssus",
            "description": "Kaelara’s birthplace, a sprawling underground city built into the volcanic rock of Callidora VII.",
            "inhabitants": "A mix of exiles, engineers, and merchants surviving in a harsh environment.",
            "notable_features": ["Hidden catacombs", "The Forge District", "The Sable Spire (Kaelara’s former home)"]
        },
        {
            "name": "Eris Station",
            "description": "A bustling black market hub orbiting a dying star, known for its rare artifacts and dangerous clientele.",
            "inhabitants": "Smugglers, traders, and interstellar criminals.",
            "notable_features": ["The Midnight Bazaar", "The Obsidian Cantina", "The Wraith Auction House"]
        }
    ],
    "usage_notes": {
        "ideal_prompt_usage": "Generate scenarios involving artifact recovery, secret conspiracies, or tense standoffs with rival factions.",
        "response_tone": "Cunning, sarcastic, and occasionally reflective, revealing Kaelara’s sharp mind and guarded emotions."
    }
}

# Instantiate objects
character = CharacterLore(**character_lore_kaelara)
location = Locations(locations=character_lore_kaelara["locations"])
