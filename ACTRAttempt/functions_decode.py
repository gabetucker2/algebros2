# SCRIPTS
import parameters
import functions_helper

# def similarity(x, y):
#     if isinstance(x, str) and isinstance(y, str):
#         # Similarity computation for string values
#         if x == y:
#             return 1.0  # Exact match
#         else:
#             return 0.0  # No match
#     elif isinstance(x, (float, int)) and isinstance(y, (float, int)):
#         # Similarity computation for float or integer values
#         if y < x:
#             return similarity(y, x)
#         return 1 - (y - x) / y
#     else:
#         return 0.0  # Default similarity for incompatible types

def similarity(x, y):
    # Ensure x and y are both numeric (float or int)
    if isinstance(x, (float, int)) and isinstance(y, (float, int)):
        # Use a normalized difference as a measure of similarity for numeric values
        if x == y:
            return 1.0  # Exact match
        max_value = max(abs(x), abs(y))
        if max_value == 0:
            return 1.0  # Both numbers are 0, consider them identical
        difference = abs(x - y)
        return max(0, 1.0 - difference / max_value)
    else:
        # Return 0.0 for non-numeric or incompatible types
        return 0.0

def decode_chunk_retrieval_strict(inputs):

    data_to_decode = functions_helper.array_to_dictionary(inputs)

    prediction = (parameters.memory.retrieve(data_to_decode, partial=False) or {}).get(parameters.OUTPUT_NAME)

    return prediction

def decode_chunk_retrieval_partial(inputs):

    data_to_decode = functions_helper.array_to_dictionary(inputs)

    # set the mismatch penalty for partial matching
    parameters.memory.mismatch = parameters.MISMATCH_PENALTY

    # call similarity functions for partial matching
    parameters.memory.similarity(
        attributes=list(data_to_decode.keys()),
        function=similarity,
        weight=parameters.SIMILARITY_WEIGHT
    )

    # Retrieve chunks with partial matching
    partial_chunks = parameters.memory.retrieve(data_to_decode, partial=True)

    # Check if any matching chunks were found
    prediction = partial_chunks.get(parameters.OUTPUT_NAME)

    return prediction

def decode_chunk_blend(inputs):

    data_to_decode = functions_helper.array_to_dictionary(inputs)

    # set the mismatch penalty for partial matching
    parameters.memory.mismatch = parameters.MISMATCH_PENALTY

    # call similarity functions for partial matching
    parameters.memory.similarity(
        attributes=list(data_to_decode.keys()),
        function=similarity,
        weight=parameters.SIMILARITY_WEIGHT
    )

    prediction, _ = parameters.memory.discrete_blend(parameters.OUTPUT_NAME, data_to_decode)

    return prediction
