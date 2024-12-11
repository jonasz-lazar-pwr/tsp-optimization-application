# src/backend/components/report_generator.py

import os
import shutil
from datetime import datetime
from pylatex import Document, Section, Subsection, Figure, NoEscape, Package
from matplotlib import pyplot as plt
from src.utils.path_config import get_path


class ReportGenerator:
    def __init__(self, instance_name: str, instance_data: dict, algorithm_results: dict, plots: dict,
                 output_path: str) -> None:
        """
        Initializes the ReportGenerator for creating a TSP optimization report in PDF format.

        :param instance_name: Name of the TSP instance.
        :param instance_data: Dictionary containing instance data (e.g., number of cities).
        :param algorithm_results: Dictionary with results for each algorithm (e.g., SA, TS).
        :param plots: Dictionary containing cost and route plots for each algorithm.
        :param output_path: Destination path where the report will be saved.
        """
        self.instance_name: str = instance_name
        self.instance_data: dict = instance_data
        self.algorithm_results: dict = algorithm_results
        self.plots: dict = plots
        self.output_path: str = output_path  # Destination path for the report

        # Paths to the best solution files for each algorithm
        self.best_solution_path_sa: str = get_path("data/best_solutions/best_solution_sa.txt")
        self.best_solution_path_ts: str = get_path("data/best_solutions/best_solution_ts.txt")

        # Temporary directory for storing plot images
        self.temp_image_directory: str = get_path("data/temp_images")

        # Ensure the temporary image directory exists
        os.makedirs(self.temp_image_directory, exist_ok=True)

    def _load_best_route(self, algorithm: str) -> list[int]:
        """
        Loads the best route from a text file corresponding to the specified algorithm.

        :param algorithm: Name of the algorithm ("SA" for Simulated Annealing or "TS" for Tabu Search).
        :return: List of city indices in the optimal route order.
        """
        try:
            # Determine file path based on the algorithm type
            file_path = self.best_solution_path_sa if algorithm == "SA" else self.best_solution_path_ts
            best_route: list[int] = []

            # Open and read each line in the best solution file
            with open(file_path, 'r') as file:
                for line in file:
                    if line.strip() == "EOF":  # End of file marker
                        break
                    best_route.append(int(line.strip()))

            return best_route
        except FileNotFoundError:
            print(f"Best solution file for {algorithm} not found.")
            return []

    def generate_report(self) -> None:
        """
        Generates a PDF report containing TSP instance details, algorithm parameters, and results.
        """
        # Initialize the LaTeX document
        doc = Document(documentclass="article", document_options="12pt")

        # Define and add LaTeX packages to the document
        packages = [
            'pifont', 'inputenc', 'xcolor', 'setspace', 'multirow', 'parskip', 'tikz', 'pdfpages', 'graphicx',
            'geometry', 'adjustbox', 'caption', 'listings', 'hyperref', 'float', 'longtable', 'tabularx',
            'rotating', 'amsmath'
        ]

        # Configure packages with options where necessary
        for package in packages:
            if package == 'xcolor':
                doc.packages.append(Package(package, options="table,xcdraw"))
            elif package == 'geometry':
                doc.packages.append(Package(package, options="left=1.0in, right=1.0in, top=0.75in, bottom=0.75in"))
            elif package == 'inputenc':
                doc.packages.append(Package(package, options="utf8"))
            elif package == 'adjustbox':
                doc.packages.append(Package(package, options="export"))
            else:
                doc.packages.append(Package(package))

        # Add a custom title with date
        title_text = "TSP Optimization Report"
        formatted_date = datetime.now().strftime(r"%Y--%m--%d %H:%M")

        doc.append(NoEscape(r"""
        \begin{center}
            \Large \textbf{""" + title_text + r"""} \\
            \vspace{0.5em}
            \normalsize """ + formatted_date + r""" \\
        \end{center}
        \vspace{1em}
            """))

        # Add section with TSP instance information
        with doc.create(Section("Instance Information")):
            doc.append(f"File name: {self.instance_name}")
            doc.append(f"\nNumber of cities: {self.instance_data.get('dimension', 'N/A')}")
            doc.append(f"\nType: TSP")
            doc.append(f"\nEdge weight type: {self.instance_data.get('edge_weight_type', 'N/A')}")
            doc.append(f"\nOptimal cost: {self.instance_data.get('optimal_length', 'N/A')}")

        # Process algorithm results and add them to the report
        for algorithm, results in self.algorithm_results.items():
            section_name = "Simulated Annealing" if algorithm == "SA" else "Tabu Search"
            with doc.create(Section(section_name)):
                # Add Parameters subsection
                with doc.create(Subsection("Parameters")):
                    params = list(results['parameters'].items())
                    for index, (param, value) in enumerate(params):
                        doc.append(f"{param}: {value}\n" if index < len(params) - 1 else f"{param}: {value}")

                # Add Results subsection
                with doc.create(Subsection("Results")):
                    doc.append(f"Best Cost: {results['best_cost']}\n")
                    doc.append(f"Relative Error: {results['relative_error']}")

        # Separate section for plots, ensuring page break
        doc.append(NoEscape(r"\newpage"))
        with doc.create(Section("Plots")):
            for algorithm in self.algorithm_results.keys():
                self._add_plots(doc, algorithm)

        # Set the TeX compiler path and save the PDF
        os.environ["PATH"] += os.pathsep + "/Library/TeX/texbin"

        # Generate PDF without .tex extension in the output path
        pdf_path = self.output_path if not self.output_path.endswith(".pdf") else self.output_path[:-4]
        doc.generate_pdf(pdf_path, clean_tex=False, compiler="pdflatex")

        # Remove the .tex file after generating the PDF
        tex_path = pdf_path + ".tex"
        if os.path.exists(tex_path):
            os.remove(tex_path)

        # Clean up temporary image files
        shutil.rmtree(self.temp_image_directory)

    def _add_plots(self, doc: Document, algorithm: str) -> None:
        """
        Adds cost and route plots for a specified algorithm to the "Plots" section in the PDF report.

        :param doc: The LaTeX Document object where the plots will be added.
        :param algorithm: The name of the algorithm ("SA" for Simulated Annealing or "TS" for Tabu Search).
        :return: None
        """
        # Set the full algorithm name based on the abbreviation
        full_name = "Simulated Annealing" if algorithm == "SA" else "Tabu Search"

        # Cost over time plot
        with doc.create(Figure(position='h!')) as cost_plot:
            # Save the cost plot as a PDF file
            plot_path = self._save_cost_plot(self.plots[algorithm]['cost_plot'], f"{algorithm}_cost_plot.pdf")
            # Add the saved plot to the document
            cost_plot.add_image(plot_path, width=NoEscape(r'0.8\textwidth'))
            cost_plot.add_caption(f"Cost over time for {full_name}")

        # Check if route coordinates are available before adding route plot
        coordinates = self.instance_data.get('coordinates') or self.instance_data.get('display_coordinates')
        if coordinates:
            with doc.create(Figure(position='h!')) as route_plot:
                # Load the best route and save the route plot as a PDF file
                best_route = self._load_best_route(algorithm)
                plot_path = self._save_route_plot(best_route, f"{algorithm}_route_plot.pdf")
                # Add the saved route plot to the document
                route_plot.add_image(plot_path, width=NoEscape(r'0.8\textwidth'))
                route_plot.add_caption(f"Best route for {full_name}")
        else:
            print(f"No coordinates available for {algorithm}; skipping route plot.")

    def _save_cost_plot(self, plot_data: dict[str, list[float]], filename: str) -> str:
        """
        Saves a cost plot as a PDF based on the provided data.

        :param plot_data: A dictionary containing the x and y data points for the cost plot.
                          Expected keys are 'x' for x-axis values and 'y' for y-axis values.
        :param filename: The name under which to save the plot file.
        :return: The full path to the saved plot file.
        """
        # Define the path for saving the plot
        plot_path = os.path.join(self.temp_image_directory, filename)

        # Set up the plot
        plt.figure()
        if 'x' in plot_data and 'y' in plot_data:
            plt.plot(plot_data['x'], plot_data['y'], color='#FF8315', linewidth=0.8)
            plt.xlabel('Time [ms]')
            plt.ylabel('Cost')
        else:
            print("Error: plot_data must contain 'x' and 'y' keys.")

        # Adjust layout for better presentation and save as PDF
        plt.tight_layout()
        plt.savefig(plot_path, format='pdf')
        plt.close()  # Close the plot to free memory

        return plot_path

    def _save_route_plot(self, route_data: list[int], filename: str) -> str:
        """
        Saves a route plot based on provided route data as a PDF.

        :param route_data: A list of city indices representing the optimal route order.
        :param filename: The name under which to save the route plot file.
        :return: The full path to the saved route plot file.
        """
        # Define the path for saving the route plot
        plot_path = os.path.join(self.temp_image_directory, filename)

        # Retrieve city coordinates from instance data
        coordinates = self.instance_data.get("coordinates") or self.instance_data.get("display_coordinates")
        if not coordinates:
            print("No coordinates available to generate the route plot.")
            return plot_path

        # Filter coordinates based on route data indices, ensuring valid indices
        city_coords = [coordinates[city_index] for city_index in route_data if city_index < len(coordinates)]
        if not city_coords:
            print("No valid city coordinates available for the route plot.")
            return plot_path

        # Close the loop by appending the start city at the end of the route
        city_coords.append(city_coords[0])
        x_coords, y_coords = zip(*city_coords)  # Separate x and y coordinates

        # Plot the route
        plt.figure()
        plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='#1F77B4', linewidth=0.8, markersize=3)
        plt.xlabel('X-coordinates')
        plt.ylabel('Y-coordinates')
        plt.tight_layout()  # Adjust layout for clean presentation
        plt.savefig(plot_path, format='pdf')  # Save the plot as a PDF
        plt.close()  # Close the plot to free memory

        return plot_path
