#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Ebbe Wertz, Robin Lambregts, Mathias Houwen"
__version__ = "2.0"
__license__ = "GPLv3"

import matplotlib.pyplot as plt
import pandas as pd
from src.model.ModelHandler import ModelHandler
from src.model.massaging_functions import massage_for_linear_regression, massage_for_grad_boost, \
    massage_for_neural_network
from src.model.models.GradientBoostingRegressionModel import GradientBoostingRegressionModel
from src.model.models.LinearRegressionModel import LinearRegressionModel
from src.model.models.NeuralNetworkSklearnModel import NeuralNetworkSklearnModel
from src.evaluation.metrics import print_mean_square, print_MAPE
from src.util.utils import make_parser_and_parse
from src.evaluation.visualisation import predicted_vs_actual_line, ape_boxplot, plot_input_data


def main(args):
    """ Main entry point of the app """

    # read data from file
    training_dataframe = pd.read_csv(args.training_file)
    testing_dataframe_raw = pd.read_csv(args.testing_file)

    # config model handler
    model_handler = ModelHandler(
        test_dataframe=testing_dataframe_raw,
        train_dataframe=training_dataframe,
        y_column='Last Close',
        model_class=LinearRegressionModel,
        # model_class=GradientBoostingRegressionModel,
        # model_class=NeuralNetworkSklearnModel,
        massaging_function=massage_for_linear_regression
        # massaging_function = massage_for_grad_boost
        # massaging_function = massage_for_neural_network
    )

    # train and predict
    model_handler.massage()
    model_handler.train()
    model_handler.predict()
    testing_dataframe_result = model_handler.getTestDataframe()

    # visualise and show metrics
    print_mean_square(testing_dataframe_result, 'Last Close')
    print_MAPE(testing_dataframe_result, 'Last Close')

    plt.figure()
    predicted_vs_actual_line(testing_dataframe_result, 'Last Close')
    plt.figure()
    ape_boxplot(testing_dataframe_result, 'Last Close')
    plt.show()


if __name__ == "__main__":
    args = make_parser_and_parse(__version__)
    main(args)
