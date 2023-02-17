from adjustText import adjust_text
from PIL import Image
import pickle
import plotly as px
from matplotlib.lines import Line2D
import matplotlib.transforms as transforms
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import pandas as pd
import numpy as np
from scipy.special import comb
import scipy.misc


def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of `x` and `y`
    See how and why this works: https://carstenschelp.github.io/2018/09/14/Plot_Confidence_Ellipse_001.html
    This function has made it into the matplotlib examples collection:
    https://matplotlib.org/devdocs/gallery/statistics/confidence_ellipse.html#sphx-glr-gallery-statistics-confidence-ellipse-py
    Or, once matplotlib 3.1 has been released:
    https://matplotlib.org/gallery/index.html#statistics
    I update this gist according to the version there, because thanks to the matplotlib community
    the code has improved quite a bit.
    Parameters
    ----------
    x, y : array_like, shape (n, )
        Input data.
    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.
    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.
    Returns
    -------
    matplotlib.patches.Ellipse
    Other parameters
    ----------------
    kwargs : `~matplotlib.patches.Patch` properties
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0),
                      width=ell_radius_x * 2,
                      height=ell_radius_y * 2,
                      facecolor=facecolor,
                      **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)

    return ax.add_patch(ellipse)
    # render plot with "plt.show()".


def fitting():
    scipy.misc.comb = comb

    pre_delta = pd.read_csv('./static_files/files/TOPdata_webfig_20221212.csv')

    # perform row-wise transformation
    pre_delta_hell = pd.concat([pre_delta.loc[:, ['pfas_source', 'pfas_source_matrix']], pre_delta.loc[:, 'prePFBA':].apply(
        lambda x: np.sqrt(x / sum(x)), axis=1)], axis=1)

    # split data
    X = pre_delta_hell.loc[:, 'prePFBA':].values
    y = pre_delta_hell.loc[:, ['pfas_source_matrix', 'pfas_source']].values

    # perform column-wise normalization
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # run PCA
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(X)

    # split off principal components
    principalDf = pd.DataFrame(data=principalComponents, columns=[
        'principal component 1', 'principal component 2'])

    # merge PCs back with labels
    pre_delta_hell.reset_index(inplace=True, drop=True)
    pre_delta_hell_pca = pd.concat(
        [pre_delta_hell.loc[:, ['pfas_source_matrix', 'pfas_source']], principalDf], axis=1)

    # define each PC's explained variance
    pre_delta_hell_pca_var1 = (pca.explained_variance_ratio_[0]*100).round(1)
    pre_delta_hell_pca_var2 = (pca.explained_variance_ratio_[1]*100).round(1)
    return [pre_delta_hell_pca, pre_delta_hell_pca_var1, pre_delta_hell_pca_var2]


def checkformat(file):
    print(file)
    df = pd.read_csv(file)
    if not all(df.columns == ['sample', 'prePFBA', 'prePFPeA', 'prePFHxA', 'prePFHpA', 'prePFOA',
       'prePFNA', 'prePFBS', 'prePFHxS', 'prePFOS', 'dPFBA', 'dPFPeA',
                              'dPFHxA', 'dPFHpA', 'dPFOA', 'dPFNA']):
        return False
    elif (df.iloc[:, 1:].values < 0).any() == True:
        return False
    else:
        return True


def userplot(file):
    scipy.misc.comb = comb

    pre_delta_hell_pca, pre_delta_hell_pca_var1, pre_delta_hell_pca_var2 = fitting()

    model = pickle.load(open('./static_files/models/model.pkl', 'rb'))
    user_samples = pd.read_csv(file)
    scaler = model[0]
    pca = model[1]

    user_samples_hell = pd.concat([user_samples.loc[:, ['sample']], user_samples.loc[:, 'prePFBA':].apply(
        lambda x: np.sqrt(x / sum(x)), axis=1)], axis=1)

    # split data
    X_user = user_samples_hell.loc[:, 'prePFBA':].values
    y_user = user_samples_hell.loc[:, ['sample']].values

    # normalize by column (note that scaler was fitted on the training data above--not here)
    X_user_hell_norm = scaler.transform(X_user)

    # perform pca (note that pca was fitted on the training data above--not here)
    # Not sure where X_user_norm is. Opted with X_user
    X_user_hell_norm_pca = pca.transform(X_user_hell_norm)

    # split off principal components
    user_pcs = pd.DataFrame(data=X_user_hell_norm_pca, columns=[
                            'principal component 1', 'principal component 2'])

    # merge PCs back with labels
    user_samples_hell.reset_index(inplace=True, drop=True)
    user_samples_pca = pd.concat(
        [user_samples_hell.loc[:, 'sample'], user_pcs], axis=1)

    fig = plt.figure(figsize=(20, 15))
    ax = fig.add_subplot(1, 1, 1)

    # create dictionaries for marker colors and shapes
    targets = ['afff_gw', 'afff_sw', 'afff_soil',
               'wwtp_inf', 'wwtp_eff', 'wwtp_biosolids', 'landfill']
    colors = ['#9bbedb', '#377eb8', '#265880', 'gold',
              'orange', 'chocolate', '#4daf4a', '#a65628', '#eb7d34']
    shapes = ['o', 'o', 'o', 'v', 'v', 'v', '*']

    color_dict = dict(zip(targets, colors))
    shape_dict = dict(zip(targets, shapes))

    # plot
    sns.scatterplot(data=pre_delta_hell_pca, x='principal component 1', y='principal component 2',
                    hue='pfas_source_matrix',
                    palette=color_dict,
                    style='pfas_source_matrix',
                    markers=shape_dict,
                    s=200)

    # Make indices for drawing 95% confidene ellipses
    afff_idx = pre_delta_hell_pca.index[pre_delta_hell_pca['pfas_source'] == 'afff'].tolist(
    )
    lndfl_idx = pre_delta_hell_pca.index[pre_delta_hell_pca['pfas_source'] == 'landfill'].tolist(
    )
    wwtp_idx = pre_delta_hell_pca.index[pre_delta_hell_pca['pfas_source'] == 'wwtp'].tolist(
    )
    idxs = [afff_idx, wwtp_idx, lndfl_idx]

    # add 95% confidence ellipse
    hull_colors = ['#377eb8', '#ff7f00', '#4daf4a']

    for idx, c in zip(idxs, hull_colors):
        pc1 = np.asarray(np.asarray(
            pre_delta_hell_pca.loc[idx, 'principal component 1']))
        pc2 = np.asarray(np.asarray(
            pre_delta_hell_pca.loc[idx, 'principal component 2']))
        confidence_ellipse(pc1, pc2, ax, n_std=2, facecolor=c, alpha=0.3)

    # add loading vectors
    features = ['PFBA', 'PFPeA', 'PFHxA', 'PFHpA', 'PFOA', 'PFNA',
                'PFBS', 'PFHxS', 'PFOS', u'ΔPFBA', u'ΔPFPeA', u'ΔPFHxA', u'ΔPFHpA',
                u'ΔPFOA', u'ΔPFNA']

    coeff = np.transpose(pca.components_[0:2, :])
    xs = pre_delta_hell_pca.loc[:, 'principal component 1']
    ys = pre_delta_hell_pca.loc[:, 'principal component 2']
    n = coeff.shape[0]
    scalex = 1.0/(xs.max() - xs.min())
    scaley = 1.0/(ys.max() - ys.min())

    for i, feat in zip(range(n), features):
        plt.arrow(0, 0, coeff[i, 0]/scalex, coeff[i, 1] /
                  scaley, color='black', alpha=0.5)
    text = [plt.text(coeff[i, 0]/scalex*1.1, coeff[i, 1]/scaley*1.1, feat, color='black',
                     ha='center', va='baseline', fontsize=15) for i, feat in zip(range(n), features)]
    adjust_text(text)
    # set labels
    ax.set_xlabel('Principal Component 1 ({}%)'.format(
        pre_delta_hell_pca_var1), fontsize=20)
    ax.set_ylabel('Principal Component 2 ({}%)'.format(
        pre_delta_hell_pca_var2), fontsize=20)

    # set ticks
    ax.tick_params(labelsize=20)

    # Add user samples
    p1 = sns.scatterplot(data=user_samples_pca, x='principal component 1', y='principal component 2',
                         s=200, color='red')

    text = [p1.text(user_samples_pca['principal component 1'][line]+0.09, user_samples_pca['principal component 2'][line],
                    user_samples_pca['sample'][line], horizontalalignment='left',
                    size='20', color='black', weight='light') for line in range(0, user_samples_pca.shape[0])]
    adjust_text(text, arrowprops=dict(arrowstyle="-", color='w'))

    # add legend
    leg = ['Airport - GW', 'Airport - SW', 'Airport - Sed',
           'WWTP - Inf', 'WWTP - Eff', 'WWTP - Bio', 'Landfill']

    legend_elements = [(Line2D([0], [0],
                               color='w',
                               markerfacecolor=colors[i],
                               marker=shapes[i],
                               markersize=14,
                               label=leg[i])) for i in range(7)]

    ax.legend(handles=legend_elements, fontsize=20)
    return fig
    # return fig2img(fig)


def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img
