import itertools

import config


table = config.TABLE
osm_table = config.OSM_TABLE
autosplit_table = config.AUTOSPLIT_TABLE


# admin_level => list of countries which should be initially divided at one admin level
unilevel_countries = {
        2: [
            'Afghanistan',
            'Albania',
            'Algeria',
            'Andorra',
            'Angola',
            'Antigua and Barbuda',
            'Armenia',
            'Australia', # need to be divided at level 4 but has many small islands of level 4
            'Azerbaijan', # has 2 non-covering 3-level regions
            'Bahrain',
            'Barbados',
            'Belize',
            'Benin',
            'Bermuda',
            'Bhutan',
            'Botswana',
            'British Sovereign Base Areas',  # ! include into Cyprus
            'British Virgin Islands',
            'Bulgaria',
            'Burkina Faso',
            'Burundi',
            'Cambodia',
            'Cameroon',
            'Cape Verde',
            'Central African Republic',
            'Chad',
            'Chile',
            'Colombia',
            'Comoros',
            'Congo-Brazzaville',  # BUG whith autodivision at level 4
            'Cook Islands',
            'Costa Rica',
            'Croatia',  # next level = 6
            'Cuba',
            'Cyprus',
            "Côte d'Ivoire",
            'Democratic Republic of the Congo',
            'Djibouti',
            'Dominica',
            'Dominican Republic',
            'East Timor',
            'Ecuador',
            'Egypt',
            'El Salvador',
            'Equatorial Guinea',
            'Eritrea',
            'Estonia',
            'Eswatini',
            'Ethiopia',
            'Falkland Islands',
            'Faroe Islands',
            'Federated States of Micronesia',
            'Fiji',
            'Gabon',
            'Georgia',
            'Ghana',
            'Gibraltar',
            'Greenland',
            'Grenada',
            'Guatemala',
            'Guernsey',
            'Guinea',
            'Guinea-Bissau',
            'Guyana',
            'Haiti',
            'Honduras',
            'Iceland',
            'Indonesia',
            'Iran',
            'Iraq',
            'Isle of Man',
            'Israel',  # ! don't forget to separate Jerusalem
            'Jamaica',
            'Jersey',
            'Jordan',
            'Kazakhstan',
            'Kenya',  # ! level 3 doesn't cover the whole country
            'Kiribati',
            'Kosovo',
            'Kuwait',
            'Kyrgyzstan',
            'Laos',
            'Latvia',
            'Lebanon',
            'Liberia',
            'Libya',
            'Liechtenstein',
            'Lithuania',
            'Luxembourg',
            'Madagascar',
            'Malaysia',
            'Maldives',
            'Mali',
            'Malta',
            'Marshall Islands',
            'Martinique',
            'Mauritania',
            'Mauritius',
            'Mexico',
            'Moldova',
            'Monaco',
            'Mongolia',
            'Montenegro',
            'Montserrat',
            'Mozambique',
            'Myanmar',
            'Namibia',
            'Nauru',
            'Nicaragua',
            'Niger',
            'Nigeria',
            'Niue',
            'North Korea',
            'North Macedonia',
            'Oman',
            'Palau',
            # ! 'Palestina' is not a country in OSM - need make an mwm
            'Panama',
            'Papua New Guinea',
            'Peru', #  need split-merge
            'Philippines',  # split at level 3 and merge or not merte
            'Qatar',
            'Romania', #  need split-merge
            'Rwanda',
            'Saint Helena, Ascension and Tristan da Cunha',
            'Saint Kitts and Nevis',
            'Saint Lucia',
            'Saint Vincent and the Grenadines',
            'San Marino',
            'Samoa',
            'Saudi Arabia',
            'Senegal',
            'Seychelles',
            'Sierra Leone',
            'Singapore',
            'Slovakia', # ! split at level 3 then 4, and add Bratislava region (4)
            'Slovenia',
            'Solomon Islands',
            'Somalia',
            'South Georgia and the South Sandwich Islands',
            'South Korea',
            'South Sudan',
            'South Ossetia',  # ! don't forget to divide from Georgia
            'Sri Lanka',
            'Sudan',
            'São Tomé and Príncipe',
            'Suriname',
            'Switzerland',
            'Syria',
            'Taiwan',
            'Tajikistan',
            'Thailand',
            'The Bahamas',
            'The Gambia',
            'Togo',
            'Tokelau',
            'Tonga',
            'Trinidad and Tobago',
            'Tunisia',
            'Turkmenistan',
            'Turks and Caicos Islands',
            'Tuvalu',
            'United Arab Emirate',
            'Uruguay',
            'Uzbekistan',
            'Vanuatu',
            'Venezuela', # level 3 not comprehensive
            'Vietnam',
            # ! don't forget 'Wallis and Futuna', belongs to France
            'Yemen',
            'Zambia',
            'Zimbabwe',
           ],
        3: [
            'Malawi',
            'Nepal',  # ! one region is lost after division
            'Pakistan',
            'Paraguay',
            'Tanzania',
            'Turkey',
            'Uganda',
           ],
        4: [
            'Austria',
            'Bangladesh',
            'Belarus',  # maybe need merge capital region with the province
            'Belgium',  # maybe need merge capital region into encompassing province
            'Bolivia',
            'Bosnia and Herzegovina', # other levels - 5, 6, 7 - are incomplete.
            'Canada',
            'China',  # ! don't forget about Macau and Hong Kong of level 3 not covered by level 4
            'Denmark',
            'Greece',  # ! has one small 3-level subregion!
            'Hungary',  # maybe multilevel division at levels [4, 5] ?
            'India',
            'Italy',
            'Japan',  # ? About 50 4-level subregions, some of which requires further division
            'Morocco',  # ! not all regions appear after substitution with level 4
            'New Zealand',  # ! don't forget islands to the north and south
            'Norway',
            'Poland',  # 380(!) subregions of AL=6
            'Portugal',
            'Russia',
            'Serbia',
            'South Africa',
            'Spain',
            'Ukraine',
            'United States',
           ],
        5: [
            'Ireland',  # ! 5-level don't cover the whole country
           ],
        6: [
            'Czechia',
           ]
}

# Country name => list of admin levels to which it should be initially divided.
# 'Germany': [4, 5] implies that the country is divided at level 4 at first, then all
#  4-level subregions are divided into subregions of level 5 (if any)
multilevel_countries = {
        'Brazil': [3, 4],
        'Finland': [3, 6], # [3,5,6] in more fresh data?   # division by level 6 seems ideal
        'France': [3, 4],
        'Germany': [4, 5],  # not the whole country is covered by units of AL=5
        'Netherlands': [3, 4], # there are carribean lands of level both 3 and 4
        'Sweden': [3, 4],  # division by level 4 seems ideal
        'United Kingdom': [4, 5],  # level 5 is necessary but not comprehensive

}

country_initial_levels = dict(itertools.chain(
    ((country, ([level] if level > 2 else []))
        for level, countries in unilevel_countries.items()
        for country in countries),
    multilevel_countries.items()
))


class CountryStructureException(Exception):
    pass


def _clear_borders(conn):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table}")
    conn.commit()


def _find_subregions(conn, osm_ids, next_level, parents, names):
    """Return subregions of level 'next_level' for regions with osm_ids."""
    cursor = conn.cursor()
    parent_osm_ids = ','.join(str(x) for x in osm_ids)
    cursor.execute(f"""
        SELECT b.osm_id, b.name, subb.osm_id, subb.name
        FROM {osm_table} b, {osm_table} subb
        WHERE subb.admin_level=%s
            AND b.osm_id IN ({parent_osm_ids})
            AND ST_Contains(b.way, subb.way)
        """,
        (next_level,)
    )

    # parent_osm_id => [(osm_id, name), (osm_id, name), ...]
    subregion_ids = []

    for rec in cursor:
        parent_osm_id = rec[0]
        osm_id = rec[2]
        parents[osm_id] = parent_osm_id
        name = rec[3]
        names[osm_id] = name
        subregion_ids.append(osm_id)
    return subregion_ids


def _create_regions(conn, osm_ids, parents, names):
    if not osm_ids:
        return
    osm_ids = list(osm_ids)  # to ensure order
    cursor = conn.cursor()
    sql_values = ','.join(
            f'({osm_id},'
             '%s,'
            f'(SELECT way FROM {osm_table} WHERE osm_id={osm_id}),'
            f'{parents[osm_id] or "NULL"},'
            'now())'
            for osm_id in osm_ids
    )
    #print(f"create regions with osm_ids={osm_ids}")
    #print(f"names={tuple(names[osm_id] for osm_id in osm_ids)}")
    #print(f"all parents={parents}")
    cursor.execute(f"""
        INSERT INTO {table} (id, name, geom, parent_id, modified)
        VALUES {sql_values}
        """, tuple(names[osm_id] for osm_id in osm_ids)
    )


def _make_country_structure(conn, country_osm_id):
    names = {}  # osm_id => osm name
    parents = {}  # osm_id => parent_osm_id

    country_name = get_osm_border_name_by_osm_id(conn, country_osm_id)
    names[country_osm_id] = country_name
    parents[country_osm_id] = None

    _create_regions(conn, [country_osm_id], parents, names)

    if country_initial_levels.get(country_name):
        admin_levels = country_initial_levels[country_name]
        prev_admin_levels = [2] + admin_levels[:-1]
        prev_region_ids = [country_osm_id]

        for admin_level, prev_level in zip(admin_levels, prev_admin_levels):
            if not prev_region_ids:
                raise CountryStructureException(
                        f"Empty prev_region_ids at {country_name}, "
                        f"AL={admin_level}, prev-AL={prev_level}"
                )
            subregion_ids = _find_subregions(conn, prev_region_ids,
                                             admin_level, parents, names)
            _create_regions(conn, subregion_ids, parents, names)
            prev_region_ids = subregion_ids


def create_countries_initial_structure(conn):
    _clear_borders(conn)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT osm_id, name
        FROM {osm_table}
        WHERE admin_level = 2
        """
        #  and name in --('Germany', 'Luxembourg', 'Austria')
        #    ({','.join(f"'{c}'" for c in country_initial_levels.keys())})
        #"""
    )
    for rec in cursor:
        _make_country_structure(conn, rec[0])
    conn.commit()

def get_osm_border_name_by_osm_id(conn, osm_id):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT name FROM {osm_table}
        WHERE osm_id = %s
        """, (osm_id,))
    rec = cursor.fetchone()
    if not rec:
        raise CountryStructureException(f'Not found region with osm_id="{osm_id}"')
    return rec[0]


def _get_country_osm_id_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT osm_id FROM {osm_table}
        WHERE admin_level = 2 AND name = %s
        """, (name,))
    row_count = cursor.rowcount
    if row_count > 1:
        raise CountryStructureException(f'More than one country "{name}"')
    rec = cursor.fetchone()
    if not rec:
        raise CountryStructureException(f'Not found country "{name}"')
    return int(rec[0])



splitting = [
    # large region name, admin_level (2 in most cases), admin_level to split'n'merge, into subregions of what admin_level
        ('Germany', 2, 4, 6),  #  Half of the country is covered by units of AL=5
        ('Metropolitan France', 3, 4, 6),
        ('Spain', 2, 4, 6),
        ('Portugal', 2, 4, 6),
        ('Belgium', 2, 4, 6),
        ('Italy', 2, 4, 6),
        ('Switzerland', 2, 2, 4),  # has admin_level=5
        ('Austria', 2, 4, 6),
        ('Poland', 2, 4, 6),  # 380(!) of AL=6
        ('Czechia', 2, 6, 7),
        ('Ukraine', 2, 4, 6),   # should merge back to region=4 level clusters
        ('United Kingdom', 2, 5, 6),  # whole country is divided by level 4; level 5 is necessary but not comprehensive
        ('Denmark', 2, 4, 7),
        ('Norway', 2, 4, 7),
        ('Sweden', 2, 4, 7),   # though division by level 4 is currently ideal
        ('Finland', 2, 6, 7),  # though division by level 6 is currently ideal
        ('Estonia', 2, 2, 6),
        ('Latvia', 2, 4, 6),  # the whole country takes 56Mb, all 6-level units should merge into 4-level clusters
        ('Lithuania', 2, 2, 4), # now Lithuania has 2 mwms of size 60Mb each
        ('Belarus', 2, 2, 4),   # 6 regions + Minsk city. Would it be merged with the region?
        ('Slovakia', 2, 2, 4),  # there are no subregions 5, 6, 7. Must leave all 8 4-level regions
        ('Hungary', 2, 5, 6),
        #('Slovenia', 2, 2, 8),  # no levels 3,4,5,6; level 7 incomplete.
        ('Croatia', 2, 2, 6),
        ('Bosnia and Herzegovina', 2, 2, 4), # other levels - 5, 6, 7 - are incomplete.
        ('Serbia', 2, 4, 6),
        ('Romania', 2, 2, 4),
        ('Bulgaria', 2, 2, 4),
        ('Greece', 2, 4, 5),   # has 7 4-level regions, must merge 5-level to them again
        ('Ireland', 2, 5, 6),  # 5-level don't cover the whole country! Still...
        ('Turkey', 2, 3, 4),
    ]