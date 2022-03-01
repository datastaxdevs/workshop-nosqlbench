""" output_handling.py """

import os


try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None


def canCreateFile(fName, overwrite):
  return overwrite or not os.path.isfile(fName)


def openFigure(w, h):
    # in-routine import for minimal dependencies on constrained installs
    fig = plt.figure(figsize=(w, h))
    return fig


def saveFigure(figure, filename):
    # in-routine import for minimal dependencies on constrained installs
    figure.savefig(filename)
    plt.close(figure)


def plotToFigure(pType, pData, hstep, metric, fName, unitName):
    # return True iff image creation succeeds
    if plt:
        if pType == 'baseplot':
            plot = openFigure(20, 14)
            xs, ys = pData[0]
            plt.bar(
                xs,
                ys,
                width=hstep,
            )
            plt.xlabel('t [%s]' % unitName)
            plt.ylabel('p(t) [1/%s]' % unitName)
            plt.ylim((0, None))
            plt.title('Distribution for "%s"' % metric)
            saveFigure(plot, fName)
            return True
        elif pType == 'stability':
            plot = openFigure(20, 14)
            curves = pData
            colors = plt.cm.winter([i/(len(curves)-1) for i in range(len(curves))])
            for sli, (xs, ys) in enumerate(curves):
                if len(xs) > 0:
                    plt.plot(
                        xs,
                        ys,
                        '-',
                        lw=3,
                        color=colors[sli],
                        label='Slice %i' % sli,
                    )
            plt.xlabel('t [%s]' % unitName)
            plt.ylabel('p(t) [1/%s]' % unitName)
            plt.ylim((0, None))
            plt.legend()
            plt.title('Stability analysis for "%s"' % metric)
            saveFigure(plot, fName)
            return True
        elif pType == 'percentiles':
            plot = openFigure(14, 20)
            xs, ys = pData[0]
            plt.plot(xs, ys, '-')
            plt.xlabel('Percentile')
            plt.ylabel('t [%s]' % unitName)
            xticks = [i for i in range(0, 110, 10)]

            def _firstOrNone(lst):
                return lst[0] if len(lst) > 0 else None

            yticks = [
                yt
                for yt in (
                    _firstOrNone([y for (x, y) in zip(xs, ys) if x >= xt])
                    for xt in xticks
                )
                if yt is not None
            ]
            plt.xticks(xticks)
            plt.yticks(yticks)
            plt.ylim((0, None))
            plt.grid()
            plt.title('Percentiles for "%s"' % metric)
            saveFigure(plot, fName)
            return True
        else:
            raise ValueError('unknown plot type "%s"' % pType)
    else:
        print('      ** matplotlib not available! **')
        return False


def plotToDatafile(pType, pData, hstep, metric, fName):
    # return True iff datafile creation succeeds
    if pType == 'baseplot':
        with open(fName, 'w') as file:
            file.write('\n'.join(
                '%e\t%e' % (x, y)
                for x, y in zip(*pData[0])
            ))
        return True
    elif pType == 'stability':
        # assume curves are padded to the same xs
        xs = pData[0][0]
        yts = zip(*[curve[1] for curve in pData])
        with open(fName, 'w') as file:
            file.write('\n'.join(
                '%e\t%s' % (
                    x,
                    '\t'.join('%e' % y for y in yt),
                )
                for x, yt in zip(*(xs, yts))
            ))
        return True
    elif pType == 'percentiles':
        with open(fName, 'w') as file:
            file.write('\n'.join(
                '%e\t%e' % (x, y)
                for x, y in zip(*pData[0])
            ))
        return True
    else:
        raise ValueError('unknown plot type "%s"' % pType)


def plotHistostats(xData, pValues, legend, metric, fName):
    # return True iff image creation succeeds
    lineStyles = [
        (0,()),
        (0, (1, 1)),
        (0, (5, 5)),
        (0, (5, 1)),
        (0, (3, 5, 1, 5)),
        (0, (3, 1, 1, 1)),
        (0, (3, 1, 1, 1, 1, 1))
    ]
    if plt:
        plot = openFigure(20, 14)
        #
        for curveIndex, curve in enumerate(legend):
            if curve in pValues:
                plt.plot(
                    xData,
                    pValues[curve],
                    linestyle=lineStyles[curveIndex % len(lineStyles)],
                    label=curve,
                )
        plt.yscale('log')
        plt.xlabel('Time since start [ms]')
        plt.ylabel('Percentile for metric [ms]')
        plt.legend()
        plt.title(metric)
        #
        saveFigure(plot, fName)
        return True
    else:
        print('      ** matplotlib not available! **')
        return False
