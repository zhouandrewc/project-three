# in the CAH (Childbirth and Adoption) data, some children have answers from multiple parents and caregivers, so we aggregate those answers

def agg_race_cah(arr):
    race_arr = []
    if 2 in arr.values:
        race_arr.append("black")
    if 4 in arr.values:
        race_arr.append("asian")
    if 1 in arr.values:
        race_arr.append("white")
    return race_arr

def agg_hispanicity(arr):
    is_hispanic = sum(map(lambda x: 1 if x >= 1 and x <=7 else 0, arr))
    return is_hispanic > 0

    # function to filter out people for whom we don't know whether they received
# a bachelor's degree

def filter_na_response(row):

    if has_bachelors(row):
        return True

    # if in 2017 they responded that their highest was associates
    degtypes = ["degtype17", "up_degtype17"]
    for feat in degtypes:
        if row[feat] >= 1 and row[feat] <= 6:
            return True

    # okay, we can do:
    # if no college degree in 15, and no school/degree by 17 then
    # we return true
    # same with 13

    # if they haven't graduated from hs, gone to college,
    # or graduated from college by 2017
    if row["grad_hs17"] == 3:
        return True
    if row["up_grad_hs17"] == 3:
        return True
    if row["wtr_college17"] == 5:
        return True
    if row["grad_college17"] == 5:
        return True

    # if their current grade indicates no degree
    if row["curr_grade17"] != 0 and row["curr_grade17"] <= 16:
        return True
    if row["up_curr_grade17"] != 0 and row["up_curr_grade17"] <= 16:
        return True

    if row["attend_college15"] == 5 and row["up_wtr_college17"] == 5:
        return True

    if row["up_degtype17"] == 1:
        return True

    # people who are in college in 2017 but have completed 1-3 yrs of college
    # have checked highest_college_yr17
    if (row["up_wtr_college17"] or row["wtr_college17"] == 1) and row["highest_college_yr17"] <= 3 and row["highest_college_yr17"] > 0:
        return True
    # if not enrolled in 15 but enrolled in 17, highest_college_yr17 = 0 probably means <1 year rather than no data
    # potentially not accurate but likely is okay
    if (row["up_wtr_college17"] or row["wtr_college17"] == 1) and row["highest_college_yr17"] == 0  and row["highest_college_yr15"] == 0 and row["enrolled15"] == 5:
        return True
    return False

def has_bachelors(row):
    degtypes = ["degtype13", "degtype15", "degtype17", "up_degtype15", "up_degtype15", "up_degtype17"]
    for feat in degtypes:
        if row[feat] >= 2 and row[feat] <= 6:
            return True

    highest = ["highest_grade13"]

    for feat in highest:
        if row[feat] == 20:
            return True

    # check whether "post-graduate work" actually means degree
    curr_grades = ["curr_grade13", "curr_grade15", "curr_grade17", "curr_grade17", "up_curr_grade15", "up_curr_grade17"]
    for feat in curr_grades:
        if row[feat] == 18:
            return True
    # are some of these people nonresponses?

    if row["degtype17"] == 1:
        return False
    return False


def get_race(num):
    if num == 1:
        return "black"
    elif num == 2:
        return "white"
    elif num==3:
        return "hispanic"
    elif num==4:
        return "asian"
    else:
        return None

def get_race_ta17(num):
    if num == 1:
        return "white"
    if num == 2:
        return "hispanic"
    if num == 3:
        return "black"
    if num == 4:
        return "asian"
    else:
        return None

def is_hispanic_cah(num):
    if num >= 1 and num <= 7:
        return True
    else:
        return False

def get_env_type(num):
    if num == 1:
        return "met_central"
    if num == 2:
        return "met_fringe"
    if num == 3 or num == 4:
        return "met_small"
    elif num == 5 or num == 7:
        return "urb_met"
    elif num == 6 or num == 8:
        return "urb_nonmet"
    elif num == 9:
        return "rural"
    else:
        return None


def get_region(num):
    if num == 1:
        return "Northeast"
    if num == 2:
        return "North Central"
    if num == 3:
        return "South"
    if num == 4:
        return "West"
    else:
        return "Other"

def live_w_both_parents(row):
    num_par = (row["live_w_mother02"] == 1 or row["live_w_mother02_pcg"] == 1) + (row["live_w_father02"] == 1 or row["live_w_father02_pcg"] == 1) + (row["live_w_smother02"] == 1 or row["stepmother02"] == 1) + (row["live_w_sfather02"] == 1 or row["stepfather02"] == 1) + (row["adopt_mother02"] == 1) + (row["adopt_father02"] == 1)
    return 1 if num_par >= 2 else 0

def is_race(race):
    def is_race_help(row):
        return 1 if row["race"] == race or row["race17_1"] == race or row["race17_2"] == race or race in row["race_code_cah_1"] or race in row["race_code_cah_2"] or race in row["race_code_cah_3"] else 0
    return is_race_help