from dataclasses import dataclass, field
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, Optional, Union, NoReturn, List
import yaml
from PyOptik.directories import sellmeier_data_path


import os


# Get a list of all filenames in the directory
material_list = [os.path.splitext(f)[0] for f in os.listdir(sellmeier_data_path) if os.path.isfile(os.path.join(sellmeier_data_path, f)) and f.endswith('.yml')]


@dataclass
class Material:
    filename: str
    coefficients: np.ndarray = field(init=False)
    wavelength_range: Optional[Tuple[float, float]] = field(init=False)
    reference: Optional[str] = field(init=False)
    formula_type: int = field(init=False)

    def __post_init__(self) -> None:
        """
        Post-initialization method to load coefficients, wavelength range, formula type, and reference from a YAML file.
        """
        self.load_coefficients()

    def load_coefficients(self) -> None:
        """
        Loads the Sellmeier coefficients, wavelength range, formula type, and reference from the specified YAML file.
        """
        file_path = sellmeier_data_path / f'{self.filename}.yml'

        with open(file_path, 'r') as file:
            parsed_yaml = yaml.safe_load(file)

        # Extract the formula type
        self.formula_type = int(parsed_yaml['DATA'][0]['type'].split()[-1])

        # Extract coefficients and ensure the list has exactly 7 coefficients by padding with zeros if necessary
        coefficients_str = parsed_yaml['DATA'][0]['coefficients']
        coefficients = list(map(float, coefficients_str.split()))
        if len(coefficients) < 7:
            coefficients.extend([0.0] * (7 - len(coefficients)))
        self.coefficients = np.array(coefficients)

        # Extract wavelength range
        if 'wavelength_range' in parsed_yaml['DATA'][0]:
            self.wavelength_range = tuple(map(float, parsed_yaml['DATA'][0]['wavelength_range'].split()))
        else:
            self.wavelength_range = None

        # Extract reference
        self.reference = parsed_yaml.get('REFERENCE', None)

    def check_wavelength_range(self, wavelength: float) -> None:
        """
        Checks if a wavelength is within the material's allowable range and raises an error if it is not.

        Args:
            wavelength (float): The wavelength to check in meters.

        Raises:
            ValueError: If the wavelength is outside the allowable range.
        """
        if self.wavelength_range is not None:
            wavelength_um = wavelength * 1e6
            min_value, max_value = self.wavelength_range
            if not min_value <= wavelength_um <= max_value:
                raise ValueError(
                    f"Wavelength {wavelength_um} µm is outside the allowable range of {min_value} µm to {max_value} µm."
                )

    def compute_refractive_index(self, wavelength: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Computes the refractive index n(λ) using the appropriate formula (either Formula 1 or Formula 2).

        Args:
            wavelength (Union[float, np.ndarray]): The wavelength λ in meters, can be a single float or a numpy array.

        Returns:
            Union[float, np.ndarray]: The refractive index n(λ) for the given wavelength or array of wavelengths.

        Raises:
            ValueError: If the wavelength is outside the specified range or if an unsupported formula type is encountered.
        """
        # Ensure that wavelength is within the allowable range if it's a single value
        if isinstance(wavelength, float):
            self.check_wavelength_range(wavelength)
        else:  # If it's an array, ensure all values are within range
            for wl in np.nditer(wavelength):
                self.check_wavelength_range(float(wl))

        # Convert wavelength to micrometers
        lambda_um = wavelength * 1e6

        # Compute the refractive index based on the formula type
        match self.formula_type:
            case 1:
                # Formula 1 computation (standard Sellmeier)
                # B0, B1, C1, B2, C2, B3, C3 = self.coefficients
                B0, B1, C1, B2, C2, B3, C3 = self.coefficients
                n_squared = (
                    B0 +
                    (B1 * lambda_um**2) / (lambda_um**2 - C1**2) +
                    (B2 * lambda_um**2) / (lambda_um**2 - C2**2) +
                    (B3 * lambda_um**2) / (lambda_um**2 - C3**2)
                )
            case 2:
                # Formula 2 computation (extended Sellmeier)
                B0, B1, C1, B2, C2, B3, C3 = self.coefficients
                n_squared = (
                    1 + B0 +
                    (B1 * lambda_um**2) / (lambda_um**2 - C1) +
                    (B2 * lambda_um**2) / (lambda_um**2 - C2) +
                    (B3 * lambda_um**2) / (lambda_um**2 - C3)
                )
            case _ :
                raise ValueError(f"Unsupported formula type: {self.formula_type}")

        # Compute the refractive index n
        print(self, n_squared)
        n = np.sqrt(n_squared)


        return n

    def plot(self, wavelength_range: Union[List[float], np.ndarray]) -> NoReturn:
        """
        Plots the refractive index as a function of wavelength over a specified range.

        Args:
            wavelength_range (Union[List[float], np.ndarray]): The range of wavelengths to plot, in meters.
        """
        if isinstance(wavelength_range, list):
            wavelength_range = np.array(wavelength_range)

        if wavelength_range.ndim != 1:
            raise ValueError("wavelength_range must be a 1D array or list of float values.")

        # Calculate the refractive index over the wavelength range
        refractive_index = self.compute_refractive_index(wavelength_range)

        # Plotting
        fig, ax = plt.subplots()
        ax.set_xlabel('Wavelength [m]')
        ax.set_ylabel('Refractive Index')
        ax.plot(wavelength_range, refractive_index.real, linewidth=2, label='Real Part')
        if np.any(refractive_index.imag):
            ax.plot(wavelength_range, refractive_index.imag, linewidth=2, linestyle='--', label='Imaginary Part')
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        plt.show()

    def __repr__(self) -> str:
        """
        Provides a formal string representation of the Material object, including key attributes.

        Returns:
            str: Formal representation of the Material object.
        """
        return (
            f"Material(filename='{self.filename}', "
            f"coefficients={self.coefficients}, "
            f"wavelength_range={self.wavelength_range}, "
            f"formula_type={self.formula_type}, "
            f"reference='{self.reference}')"
        )

    def __str__(self) -> str:
        """
        Provides an informal string representation of the Material object.

        Returns:
            str: Informal representation of the Material object.
        """
        return f"Material: {self.filename}"