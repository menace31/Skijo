def min_card_in_grid(grid, col = None , row = None):
    min_value = float('inf')
    min_card_name = None
    for card_name, card in grid.items():
        number = int(card_name.split("_")[1])
        if ((number-1) % 4 == col or col is None) and (int((number-1) / 4) == row or row is None):
            if not card.get("removed", False) and card.get("visible", True) and card.get("value", float('inf')) < min_value:
                min_value = card["value"]
                min_card_name = card_name
    return {"name": min_card_name, "value": min_value}

def max_card_in_grid(grid, col = None , row = None, except_values = []):
    """
    Docstring for max_card_in_grid function.
    This function finds the card with the maximum value in the provided grid.
    :param grid: A dictionary representing the player's grid of cards.
    :param col: (Optional) The column index to filter cards. If None, all columns are considered.
    :param row: (Optional) The row index to filter cards. If None, all rows are considered.
    
    """
    max_value = float('-inf')
    max_card_name = None
    for card_name, card in grid.items():
        number = int(card_name.split("_")[1])
        if ((number-1) % 4 == col or col is None) and (int((number-1) / 4) == row or row is None):
            if not card.get("removed", False) and card.get("visible", True) and card.get("value", float('-inf')) > max_value and card.get("value") not in except_values:
                max_value = card["value"]
                max_card_name = card_name
    return {"name": max_card_name, "value": max_value}


def equal_card_in_grid(grid, target_value):
    equal_cards = [[], [], [], []]
    for card_name, card in grid.items():
        if card.get("value") == target_value and not card.get("removed", False):
            number = int(card_name.split("_")[1])
            equal_cards[(number-1) % 4].append(card_name)
    max_len = 0
    for i in equal_cards:
        if len(i) > max_len:
            max_len = len(i)
    return equal_cards,max_len


grid = {
        "carte_1": { "visible": True, "value": -1, "removed": False },
        "carte_2": { "visible": True, "value": 4, "removed": False },
        "carte_3": { "visible": False, "value": "hidden", "removed": False },
        "carte_4": { "visible": False, "value": 0, "removed": False },
        "carte_5": { "visible": True, "value": 4, "removed": False },
        "carte_6": { "visible": False, "value": 4, "removed": False },
        "carte_7": { "visible": False, "value": -2, "removed": False },
        "carte_8": { "visible": False, "value": "hidden", "removed": False },
        "carte_9": { "visible": False, "value": 10, "removed": False },
        "carte_10": { "visible": False, "value": 4, "removed": False },
        "carte_11": { "visible": False, "value": "hidden", "removed": False },
        "carte_12": { "visible": False, "value": "hidden", "removed": False }
}

print(equal_card_in_grid(grid, 4))