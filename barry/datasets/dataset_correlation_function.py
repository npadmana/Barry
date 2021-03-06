import logging

from barry.datasets.dataset_correlation_function_abc import CorrelationFunction


class CorrelationFunction_SDSS_DR12_Z061_NGC(CorrelationFunction):
    """ Correlation function for SDSS BOSS DR12 sample for the NGC with mean redshift z = 0.61    """

    def __init__(self, name=None, min_dist=30, max_dist=200, recon=True, reduce_cov_factor=1, realisation=None, isotropic=True):
        super().__init__(
            "sdss_dr12_z061_corr_ngc.pkl",
            name=name,
            min_dist=min_dist,
            max_dist=max_dist,
            recon=recon,
            reduce_cov_factor=reduce_cov_factor,
            realisation=realisation,
            isotropic=isotropic,
        )


class CorrelationFunction_ROSS_DR12_Z038(CorrelationFunction):
    """ Anisotropic Correlation function for SDSS BOSS DR12 sample from Ross 2017 with mean redshift z = 0.38    """

    def __init__(self, name=None, min_dist=30, max_dist=200, recon=True, reduce_cov_factor=1, realisation=None, isotropic=True):
        if not recon:
            raise NotImplementedError("Pre-recon data not available for ROSS_DR12_Z038")
        super().__init__(
            "ross_2016_dr12_combined_corr_zbin0p38.pkl",
            name=name,
            min_dist=min_dist,
            max_dist=max_dist,
            recon=recon,
            reduce_cov_factor=reduce_cov_factor,
            num_mocks=1000,
            realisation=realisation,
            isotropic=isotropic,
        )


class CorrelationFunction_ROSS_DR12_Z051(CorrelationFunction):
    """ Anisotropic Correlation function for SDSS BOSS DR12 sample from Ross 2017 with mean redshift z = 0.51    """

    def __init__(self, name=None, min_dist=30, max_dist=200, recon=True, reduce_cov_factor=1, realisation=None, isotropic=True):
        if not recon:
            raise NotImplementedError("Pre-recon data not available for ROSS_DR12_Z051")
        super().__init__(
            "ross_2016_dr12_combined_corr_zbin0p51.pkl",
            name=name,
            min_dist=min_dist,
            max_dist=max_dist,
            recon=recon,
            reduce_cov_factor=reduce_cov_factor,
            num_mocks=1000,
            realisation=realisation,
            isotropic=isotropic,
        )


class CorrelationFunction_ROSS_DR12_Z061(CorrelationFunction):
    """ Anisotropic Correlation function for SDSS BOSS DR12 sample from Ross 2017 with mean redshift z = 0.61    """

    def __init__(self, name=None, min_dist=30, max_dist=200, recon=True, reduce_cov_factor=1, realisation=None, isotropic=True):
        if not recon:
            raise NotImplementedError("Pre-recon data not available for ROSS_DR12_Z061")
        super().__init__(
            "ross_2016_dr12_combined_corr_zbin0p61.pkl",
            name=name,
            min_dist=min_dist,
            max_dist=max_dist,
            recon=recon,
            reduce_cov_factor=reduce_cov_factor,
            num_mocks=1000,
            realisation=realisation,
            isotropic=isotropic,
        )


if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import numpy as np

    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)7s |%(funcName)20s]   %(message)s")
    logging.getLogger("matplotlib").setLevel(logging.ERROR)

    # Make plots of the different datasets we expect to be there; the mean and errors, and 10 random realisations
    nrealisations = 10
    cmap = plt.cm.get_cmap("viridis", nrealisations)

    isotropic = False
    datasets = [
        CorrelationFunction_ROSS_DR12_Z038(isotropic=isotropic),
        CorrelationFunction_ROSS_DR12_Z051(isotropic=isotropic),
        CorrelationFunction_ROSS_DR12_Z061(isotropic=isotropic),
    ]
    for dataset in datasets:
        data = dataset.get_data()
        plt.errorbar(
            data[0]["dist"],
            data[0]["dist"] ** 2 * data[0]["xi0"],
            yerr=data[0]["dist"] ** 2 * np.sqrt(np.diag(data[0]["cov"])[: len(data[0]["dist"])]),
            fmt="o",
            c="r",
            zorder=1,
            label=r"$\xi_{0}$",
        )
        if not isotropic:
            plt.errorbar(
                data[0]["dist"],
                data[0]["dist"] ** 2 * data[0]["xi2"],
                yerr=data[0]["dist"] ** 2 * np.sqrt(np.diag(data[0]["cov"])[len(data[0]["dist"]) :]),
                fmt="o",
                c="b",
                zorder=1,
                label=r"$\xi_{2}$",
            )
        plt.xlabel(r"$s$")
        plt.ylabel(r"$s^{2}\xi_{\ell}(s)$")
        plt.title(dataset.name)
        plt.legend()
        plt.show()

    if True:
        for r in [True, False]:
            t = "Recon" if r else "Prerecon"
            datasets = [CorrelationFunction_SDSS_DR12_Z061_NGC(recon=r), CorrelationFunction_SDSS_DR12_Z061_NGC(recon=r)]
            for dataset in datasets:
                data = dataset.get_data()
                plt.errorbar(
                    data[0]["dist"],
                    data[0]["dist"] ** 2 * data[0]["xi0"],
                    yerr=data[0]["dist"] ** 2 * np.sqrt(np.diag(data[0]["cov"])),
                    fmt="o",
                    c="k",
                    zorder=1,
                )
                for i, realisation in enumerate(np.random.randint(999, size=10)):
                    dataset.set_realisation(realisation)
                    data = dataset.get_data()
                    plt.errorbar(data[0]["dist"], data[0]["dist"] ** 2 * data[0]["xi0"], fmt="-", c=cmap(i), zorder=0)
                plt.xlabel(r"$s$")
                plt.ylabel(r"$s^{2}\xi(s)$")
                plt.title(dataset.name)

                plt.show()
