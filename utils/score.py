"""
Made with hearth by Emili Bonet i Cervera
"""

def compute_scores(item, weights):
    """
    product: dict with information of the product.
    weights: dict with the customized weights for the user.
    """
    assert(sum([w for _,w in weights['nutri'].items()]) == 1 and sum([w for _,w in weights['envir'].items()]) == 1)

    baselines = {
        'envir': {
            'water': [200, 400],
            'energy': [0, 300],
            'co2': [0, 2.9],
        },
        'nutri': {
            'vitamins': [0, 100],
            'fiber': [1, 2.8],
            'calories': [0, 116.4],
            'sodium': [0, 80]
        }
    }

    # Nutritional scores
    vitamin_score = (sum([item['nutritionalInformation'][key] for key in item['nutritionalInformation'] if 'vitamin' in key]) - baselines['nutri']['vitamins'][0]) / (baselines['nutri']['vitamins'][1] - baselines['nutri']['vitamins'][0])
    fiber_score = (item['nutritionalInformation']['fiber'] - baselines['nutri']['fiber'][0]) / (baselines['nutri']['fiber'][1] - baselines['nutri']['fiber'][0])
    caloric_score = 1 - (item['nutritionalInformation']['calories'] - baselines['nutri']['calories'][0]) / (baselines['nutri']['calories'][1] - baselines['nutri']['calories'][0])
    sodium_score = 1 - (item['nutritionalInformation']['sodium'] - baselines['nutri']['sodium'][0]) / (baselines['nutri']['sodium'][1] - baselines['nutri']['sodium'][0])

    nutri_score = weights['nutri']['vitamins']*vitamin_score \
                + weights['nutri']['fiber']*fiber_score \
                + weights['nutri']['calories']*caloric_score \
                + weights['nutri']['sodium']*sodium_score

    # Environmental scores
    water_score = 1 - (item['growingInformation']['waterUsage'] - baselines['envir']['water'][0]) / (baselines['envir']['water'][1] - baselines['envir']['water'][0])
    energy_score = 1 - (item['growingInformation']['energyUsage'] - baselines['envir']['energy'][0]) / (baselines['envir']['energy'][1] - baselines['envir']['energy'][0])
    co2_score = 1 - (item['growingInformation']['co2Emissions'] - baselines['envir']['co2'][0]) / (baselines['envir']['co2'][1] - baselines['envir']['co2'][0])

    env_score = weights['envir']['water']*water_score \
              + weights['envir']['energy']*energy_score \
              + weights['envir']['co2']*co2_score

    total_score = weights['total']*env_score + (1-weights['total'])*nutri_score
    return {
        'personalized': total_score,
        'environmental': {
            'overall': env_score,
            'vitamin': vitamin_score,
            'fiber': fiber_score,
            'caloric': caloric_score,
            'sodium': sodium_score,
        },
        'nutritional': {
            'overall': nutri_score,
            'water': water_score,
            'energy': energy_score,
            'co2': co2_score
        }
    }