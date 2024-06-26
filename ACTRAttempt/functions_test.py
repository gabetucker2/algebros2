# LIBRARIES
import random

# SCRIPTS
import parameters
import functions_helper

def test(dataset, trial_probability, decode_function):

    dataset_name = dataset["name"]
    train = dataset["train"]
    test = dataset["test"]

    print(f"BEGINNING TESTING THE `{dataset_name}` DATASET")

    trial_errors = 0
    processed_trials = 0
    total_trials = test.shape[0]
    print_interval = [(i+1) * (total_trials // 10) for i in range(10)]

    for trial in range(total_trials):

        if trial in print_interval:
            print(f"{(print_interval.index(trial)+1)*10}% tested")

        if trial_probability > random.random():

            testing_inputs = test.iloc[trial, dataset["input_idxs"]]
            testing_actual = test.iloc[trial, dataset["output_idx"]]
            if parameters.BINARY:
                testing_actual = testing_actual == dataset["binary_target"]
            testing_predicted = decode_function(testing_inputs)
            trial_errors += abs(testing_predicted-testing_actual)
            print(f"predicted: {testing_predicted} | actual: {testing_actual} | error: {abs(testing_predicted-testing_actual)}")
            processed_trials += 1
    
    if processed_trials == 0:
        error_probability = -1
    else:
        error_probability = trial_errors / processed_trials
    
    # get target types for printing purposes
    target_kinds = {}
    for target_name in train.values[:, dataset["output_idx"]]:
        target_kinds[target_name] = 0
    
    print(f"Average error: {error_probability}")
    print(f"FINISHED TESTING THE `{dataset_name}` DATASET WITH {processed_trials} TRIALS ({functions_helper.get_percent(trial_probability)} OF TOTAL TRIALS) WITH {functions_helper.get_percent(parameters.MEMORY_NOISE)} NOISE AND `{len(target_kinds.keys())}` `{parameters.OUTPUT_NAME}` KINDS")

    return error_probability
