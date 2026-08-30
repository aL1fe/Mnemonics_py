"""add dictionary words

Revision ID: ff4c2a91d731
Revises: e37db67571cc
Create Date: 2026-08-30 14:40:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ff4c2a91d731"
down_revision: Union[str, Sequence[str], None] = "e37db67571cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add words to main_dictionary."""
    dictionary_table = sa.table(
        "main_dictionary",
        sa.column("eng_word", sa.String(length=100)),
        sa.column("ukr_word", sa.Unicode(length=100)),
    )

    op.bulk_insert(
        dictionary_table,
        [
            {"eng_word": "in", "ukr_word": "в"},
            {"eng_word": "on", "ukr_word": "на"},
            {"eng_word": "under", "ukr_word": "під"},
            {"eng_word": "behind", "ukr_word": "за, позаду"},
            {"eng_word": "in front of", "ukr_word": "перед"},
            {"eng_word": "next to", "ukr_word": "поруч із"},
            {"eng_word": "between", "ukr_word": "між"},
            {"eng_word": "above", "ukr_word": "над, вище"},
            {"eng_word": "near", "ukr_word": "поруч, біля"},
            {"eng_word": "after", "ukr_word": "після"},
            {"eng_word": "with", "ukr_word": "з"},
            {"eng_word": "shower", "ukr_word": "душ"},
            {"eng_word": "then", "ukr_word": "потім"},
            {"eng_word": "breakfast", "ukr_word": "сніданок"},
            {"eng_word": "outside", "ukr_word": "зовні, на вулиці"},
            {"eng_word": "noon", "ukr_word": "полудень"},
            {
                "eng_word": "exercise",
                "ukr_word": "вправа, фізичні вправи",
            },
            {"eng_word": "excited", "ukr_word": "схвильований"},
            {"eng_word": "tired", "ukr_word": "втомлений"},
            {"eng_word": "surprised", "ukr_word": "здивований"},
            {"eng_word": "coke", "ukr_word": "кока-кола"},
            {"eng_word": "adore", "ukr_word": "обожнювати"},
            {"eng_word": "wine", "ukr_word": "вино"},
            {"eng_word": "lettuce", "ukr_word": "салат-латук"},
            {"eng_word": "newspapers", "ukr_word": "газети"},
            {"eng_word": "midnight", "ukr_word": "північ"},
            {
                "eng_word": "dancer",
                "ukr_word": "танцюрист / танцівниця",
            },
            {"eng_word": "speak", "ukr_word": "говорити"},
            {
                "eng_word": "ride a bike",
                "ukr_word": "кататися на велосипеді",
            },
            {"eng_word": "weehends", "ukr_word": "вихідні"},
            {"eng_word": "visit", "ukr_word": "відвідувати, навідувати"},
            {"eng_word": "before", "ukr_word": "до, перед"},
            {"eng_word": "becase", "ukr_word": "тому що"},
            {"eng_word": "early", "ukr_word": "рано, ранній"},
            {"eng_word": "a little bit", "ukr_word": "трохи"},
            {
                "eng_word": "computer game",
                "ukr_word": "комп’ютерна гра",
            },
            {"eng_word": "carrots", "ukr_word": "морква"},
            {"eng_word": "dive", "ukr_word": "пірнати, занурюватися"},
            {"eng_word": "about", "ukr_word": "про, приблизно"},
            {"eng_word": "shy", "ukr_word": "сором’язливий"},
            {"eng_word": "proud", "ukr_word": "гордий"},
            {
                "eng_word": "worried",
                "ukr_word": "стурбований, схвильований",
            },
            {"eng_word": "embarrassed", "ukr_word": "зніяковілий"},
            {"eng_word": "dinner", "ukr_word": "вечеря"},
            {"eng_word": "busy", "ukr_word": "зайнятий"},
            {
                "eng_word": "cereal",
                "ukr_word": "пластівці, сухий сніданок",
            },
            {"eng_word": "art", "ukr_word": "мистецтво"},
            {"eng_word": "subjects", "ukr_word": "предмети"},
            {"eng_word": "magazine", "ukr_word": "журнал"},
            {"eng_word": "afraid", "ukr_word": "наляканий, боятися"},
            {
                "eng_word": "full of energy",
                "ukr_word": "сповнений енергії",
            },
            {
                "eng_word": "cbean",
                "ukr_word": "чистий / прибирати",
            },
            {"eng_word": "tidy", "ukr_word": "охайний, акуратний"},
            {"eng_word": "shoes", "ukr_word": "взуття"},
            {"eng_word": "jacket", "ukr_word": "куртка, піджак"},
            {"eng_word": "there", "ukr_word": "там"},
            {"eng_word": "picture", "ukr_word": "картинка, фотографія"},
            {
                "eng_word": "hiding",
                "ukr_word": "ховання, той, хто ховається",
            },
            {"eng_word": "everything", "ukr_word": "все"},
            {
                "eng_word": "right",
                "ukr_word": "правильний, вірний; праворуч",
            },
            {"eng_word": "butterfy", "ukr_word": "метелик"},
            {"eng_word": "always", "ukr_word": "завжди"},
            {"eng_word": "usually", "ukr_word": "зазвичай"},
            {"eng_word": "often", "ukr_word": "часто"},
            {"eng_word": "sometmes", "ukr_word": "іноді"},
            {"eng_word": "rarely", "ukr_word": "рідко"},
            {"eng_word": "never", "ukr_word": "ніколи"},
            {"eng_word": "habits", "ukr_word": "звички"},
            {"eng_word": "daily", "ukr_word": "щоденний, щодня"},
            {
                "eng_word": "routines",
                "ukr_word": "розпорядок, звичний порядок дій",
            },
            {"eng_word": "facts", "ukr_word": "факти"},
        ],
    )


def downgrade() -> None:
    """Remove dictionary words."""
    dictionary_table = sa.table(
        "main_dictionary",
        sa.column("eng_word", sa.String(length=100)),
    )

    words = [
        "in",
        "on",
        "under",
        "behind",
        "in front of",
        "next to",
        "between",
        "above",
        "near",
        "after",
        "with",
        "shower",
        "then",
        "breakfast",
        "outside",
        "noon",
        "exercise",
        "excited",
        "tired",
        "surprised",
        "coke",
        "adore",
        "wine",
        "lettuce",
        "newspapers",
        "midnight",
        "dancer",
        "speak",
        "ride a bike",
        "weehends",
        "visit",
        "before",
        "becase",
        "early",
        "a little bit",
        "computer game",
        "carrots",
        "dive",
        "about",
        "shy",
        "proud",
        "worried",
        "embarrassed",
        "dinner",
        "busy",
        "cereal",
        "art",
        "subjects",
        "magazine",
        "afraid",
        "full of energy",
        "cbean",
        "tidy",
        "shoes",
        "jacket",
        "there",
        "picture",
        "hiding",
        "everything",
        "right",
        "butterfy",
        "always",
        "usually",
        "often",
        "sometmes",
        "rarely",
        "never",
        "habits",
        "daily",
        "routines",
        "facts",
    ]

    op.execute(
        sa.delete(dictionary_table).where(
            dictionary_table.c.eng_word.in_(words)
        )
    )
