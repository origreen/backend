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
    
    nutri_sum = weights['parameters']['nutritional']['parameters']['vitamin']['weight'] + weights['parameters']['nutritional']['parameters']['fiber']['weight'] + weights['parameters']['nutritional']['parameters']['caloric']['weight'] + weights['parameters']['nutritional']['parameters']['sodium']['weight']
    vitamin_weight = weights['parameters']['nutritional']['parameters']['vitamin']['weight'] / nutri_sum
    fiber_weight = weights['parameters']['nutritional']['parameters']['fiber']['weight'] / nutri_sum
    caloric_weight = weights['parameters']['nutritional']['parameters']['caloric']['weight'] / nutri_sum
    sodium_weight = weights['parameters']['nutritional']['parameters']['sodium']['weight'] / nutri_sum
    
    nutritional_score = vitamin_weight*vitamin_score \
            + fiber_weight*fiber_score \
            + caloric_weight*caloric_score \
            + sodium_weight*sodium_score

    # Environmental scores
    water_score = 1 - (item['growingInformation']['waterUsage'] - baselines['environmental']['water'][0]) / (baselines['environmental']['water'][1] - baselines['environmental']['water'][0])
    energy_score = 1 - (item['growingInformation']['energyUsage'] - baselines['environmental']['energy'][0]) / (baselines['environmental']['energy'][1] - baselines['environmental']['energy'][0])
    co2_score = 1 - (item['growingInformation']['co2Emissions'] - baselines['environmental']['co2'][0]) / (baselines['environmental']['co2'][1] - baselines['environmental']['co2'][0])
    envir_sum = weights['parameters']['environmental']['parameters']['water']['weight'] + weights['parameters']['environmental']['parameters']['energy']['weight'] + weights['parameters']['environmental']['parameters']['co2']['weight']
    
    water_weight = weights['parameters']['environmental']['parameters']['water']['weight'] / envir_sum
    energy_weight = weights['parameters']['environmental']['parameters']['energy']['weight'] / envir_sum
    co2_weight = weights['parameters']['environmental']['parameters']['co2']['weight'] / envir_sum

    environmental_score = water_weight*water_score \
              + energy_weight*energy_score \
              + co2_weight*co2_score

    total_sum = weights['parameters']['environmental']['weight'] + weights['parameters']['nutritional']['weight']
    environmental_weight = weights['parameters']['environmental']['weight'] / total_sum
    nutritional_weight = weights['parameters']['nutritional']['weight'] / total_sum
    total_score = environmental_weight*environmental_score + nutritional_weight*nutritional_score
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
