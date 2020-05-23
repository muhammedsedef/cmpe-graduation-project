from collections import Counter
from sklearn.manifold import TSNE
from bokeh.plotting import figure, output_file, show
from bokeh.models import Label, HoverTool, Legend, value, LabelSet, ColumnDataSource
from bokeh.io import output_notebook
from bokeh.resources import CDN
from bokeh.embed import json_item, file_html
import numpy as np

def tsne_graph(output, topic_names, doc_names):
    n_topics = len(topic_names)
    topic_distributions = output.get('topic_distributions')
    data_tokens = output.get('data_tokens')

    colorArray = [
        "#63b598", "#ce7d78", "#ea9e70", "#0d5ac1",
        "#14a9ad", "#4ca2f9",
        "#d298e2", "#6119d0", "#d2737d", "#c0a43c", "#f2510e",
        "#651be6", "#79806e", "#cd2f00", "#9348af",
        "#c5a4fb", "#996635", "#b11573", "#4bb473", "#75d89e",
        "#2f3f94", "#2f7b99", "#da967d", "#34891f", "#ca4751",
        "#4b5bdc", "#250662", "#cb5bea", "#228916",
        "#ac3e1b", "#df514a", "#539397", "#880977", "#f697c1",
        "#f158bf", "#e145ba", "#ee91e3", "#4834d0",
        "#802234", "#6749e8", "#8fb413", "#b2b4f0",
        "#c3c89d", "#c9a941", "#41d158", "#fb21a3", "#51aed9",
        "#5bb32d", "#0807fb", "#21538e", "#89d534", "#d36647",
        "#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422",
        "#983f7a", "#ea24a3", "#79352c", "#521250", "#c79ed2",
        "#63b598", "#ce7d78", "#ea9e70", "#0d5ac1",
        "#14a9ad", "#4ca2f9",
        "#d298e2", "#6119d0", "#d2737d", "#c0a43c", "#f2510e",
        "#651be6", "#79806e", "#cd2f00", "#9348af",
        "#c5a4fb", "#996635", "#b11573", "#4bb473", "#75d89e",
        "#2f3f94", "#2f7b99", "#da967d", "#34891f", "#ca4751",
        "#4b5bdc", "#250662", "#cb5bea", "#228916",
        "#ac3e1b", "#df514a", "#539397", "#880977", "#f697c1",
        "#f158bf", "#e145ba", "#ee91e3", "#4834d0",
        "#802234", "#6749e8", "#8fb413", "#b2b4f0",
        "#c3c89d", "#c9a941", "#41d158", "#fb21a3", "#51aed9",
        "#5bb32d", "#0807fb", "#21538e", "#89d534", "#d36647",
        "#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422",
        "#983f7a", "#ea24a3", "#79352c", "#521250", "#c79ed2",
        "#63b598", "#ce7d78", "#ea9e70", "#0d5ac1",
        "#14a9ad", "#4ca2f9",
        "#d298e2", "#6119d0", "#d2737d", "#c0a43c", "#f2510e",
        "#651be6", "#79806e", "#cd2f00", "#9348af",
        "#c5a4fb", "#996635", "#b11573", "#4bb473", "#75d89e",
        "#2f3f94", "#2f7b99", "#da967d", "#34891f", "#ca4751",
        "#4b5bdc", "#250662", "#cb5bea", "#228916",
        "#ac3e1b", "#df514a", "#539397", "#880977", "#f697c1",
        "#f158bf", "#e145ba", "#ee91e3", "#4834d0",
        "#802234", "#6749e8", "#8fb413", "#b2b4f0",
        "#c3c89d", "#c9a941", "#41d158", "#fb21a3", "#51aed9",
        "#5bb32d", "#0807fb", "#21538e", "#89d534", "#d36647",
        "#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422",
        "#983f7a", "#ea24a3", "#79352c", "#521250", "#c79ed2"]
    freq_per_doc = []
    for document in data_tokens:
        most_vocab = Counter()
        for word in document:
            most_vocab[word] += 1
        freq_per_doc.append([word_tuple[0] for word_tuple in most_vocab.most_common(3)])

    topic_weights = []
    for document in topic_distributions:
        topic_weights.append([topic[1] for topic in document])

    colorArrayy = np.array(colorArray)
    topic_num = np.argmax(topic_weights, axis=1)
    tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99, init='pca')
    tsne_lda = tsne_model.fit_transform(topic_weights)

    labelss = np.array(topic_names)
    source = ColumnDataSource(dict(
        x=tsne_lda[:, 0],
        y=tsne_lda[:, 1],
        color=colorArrayy[topic_num],
        labels=labelss[topic_num],
        content=doc_names,
        frequent_words=freq_per_doc))
    TOOLTIPS = [
        ("index", "$index"),
        ("desc", "@content"),
        ("Keywords", "@frequent_words")]

    plot = figure(title="t-SNE Clustering of {} LDA Topics".format(n_topics),
                  plot_width=900,
                  plot_height=700,
                  tools="pan,wheel_zoom,box_zoom,reset,hover",
                  min_border=1,
                  tooltips=TOOLTIPS
                  )

    plot.scatter(x='x',
                 y='y',
                 source=source,
                 color='color',
                 legend='labels',
                 alpha=0.9,
                 size=10
                 )
    # hover tools
    hover = plot.select(dict(type=HoverTool))
    # hover.tooltips = {"content": "Title: @title"}
    plot.legend.location = "top_left"
    return file_html(plot, CDN, "tsne_lda_graph")