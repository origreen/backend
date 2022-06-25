"""
Made with hearth by Emili Bonet i Cervera
"""

def compute_scores(item, weights):
    """
    product: dict with information of the product.
    weights: dict with the customized weights for the user.
    """
    # assert(sum([w for _,w in weights['parameters']['nutritional'].items()]) == 1 and sum([w for _,w in weights['parameters']['environmental'].items()]) == 1)

    baselines = {
        'environmental': {
            'water': [200, 400],
            'energy': [0, 300],
            'co2': [0, 2.9],
        },
        'nutritional': {
            'vitamins': [0, 100],
            'fiber': [1, 2.8],
            'calories': [0, 116.4],
            'sodium': [0, 80]
        }
    }

    # Nutritional scores
    vitamin_score = (sum([item['nutritionalInformation'][key] for key in item['nutritionalInformation'] if 'vitamin' in key]) - baselines['nutritional']['vitamins'][0]) / (baselines['nutritional']['vitamins'][1] - baselines['nutritional']['vitamins'][0])
    fiber_score = (item['nutritionalInformation']['fiber'] - baselines['nutritional']['fiber'][0]) / (baselines['nutritional']['fiber'][1] - baselines['nutritional']['fiber'][0])
    caloric_score = 1 - (item['nutritionalInformation']['calories'] - baselines['nutritional']['calories'][0]) / (baselines['nutritional']['calories'][1] - baselines['nutritional']['calories'][0])
    sodium_score = 1 - (item['nutritionalInformation']['sodium'] - baselines['nutritional']['sodium'][0]) / (baselines['nutritional']['sodium'][1] - baselines['nutritional']['sodium'][0])

    nutritional_score = weights['parameters']['nutritional']['parameters']['vitamins']['weight']*vitamin_score \
                + weights['parameters']['nutritional']['parameters']['fiber']['weight']*fiber_score \
                + weights['parameters']['nutritional']['parameters']['calories']['weight']*caloric_score \
                + weights['parameters']['nutritional']['parameters']['sodium']['weight']*sodium_score

    # Environmental scores
    water_score = 1 - (item['growingInformation']['waterUsage'] - baselines['environmental']['water'][0]) / (baselines['environmental']['water'][1] - baselines['environmental']['water'][0])
    energy_score = 1 - (item['growingInformation']['energyUsage'] - baselines['environmental']['energy'][0]) / (baselines['environmental']['energy'][1] - baselines['environmental']['energy'][0])
    co2_score = 1 - (item['growingInformation']['co2Emissions'] - baselines['environmental']['co2'][0]) / (baselines['environmental']['co2'][1] - baselines['environmental']['co2'][0])

    environmental_score = weights['parameters']['environmental']['parameters']['water']['weight']*water_score \
              + weights['parameters']['environmental']['parameters']['energy']['weight']*energy_score \
              + weights['parameters']['environmental']['parameters']['co2']['weight']*co2_score

    total_score = weights['parameters']['environmental']['weight']*environmental_score + weights['parameters']['nutritional']['weight']*nutritional_score
    return {
        'personalized': total_score,
        'nutritional': {
            'overall': nutritional_score,
            'vitamin': vitamin_score,
            'fiber': fiber_score,
            'caloric': caloric_score,
            'sodium': sodium_score,
        },
        'environmental': {
            'overall': environmental_score,
            'water': water_score,
            'energy': energy_score,
            'co2': co2_score
        }
    }