adm = Avidemux()
ed=Editor()
gui=Gui()

# Populate the part below based on the project script
# exported once editing is finished.
# Audio-related commands may be completely omitted if
# there are no special wishes like track language etc.
#
# Alternatively, load a video, perform editing, select
# encoder etc, then run this script.
# ---------------------------------------------------
# if not adm.loadVideo("/path/to/video"):
#    raise("Cannot load /path/to/video")
#adm.audioClearTracks()
#adm.setSourceTrackLanguage(0,"eng")
#if adm.audioTotalTracksCount() <= 0:
#    raise("Cannot add audio track 0, total tracks: " + str(adm.audioTotalTracksCount()))
#adm.audioAddTrack(0)
#adm.audioCodec(0, "copy")
#adm.audioSetShift(0, 0, 0)
#adm.clearSegments()
#adm.addSegment(0, 17304033, 368451423)
#adm.addSegment(0, 427030022, 463262800)
#adm.addSegment(0, 1050285989, 443860078)
#adm.addSegment(0, 1639324433, 362645623)
#adm.addSegment(0, 2185019589, 416582833)
#adm.addSegment(0, 2657341433, 392925867)
#adm.addSegment(0, 3180330567, 406038966)
#adm.addSegment(0, 3640990767, 450733622)
#adm.addSegment(0, 4162027956, 438438000)
#adm.addSegment(0, 4820585856, 475007866)
#adm.addSegment(0, 5435850500, 446796356)
#adm.addSegment(0, 6110891533, 454287167)
#adm.addSegment(0, 6695542267, 481264122)

#adm.videoCodec("x265", "useAdvancedConfiguration=True", "general.params=AQ=21", "general.poolThreads=99", "general.frameThreads=0", "general.output_bit_depth=0", "general.preset=medium", "general.tuning=animation", "general.profile=main"
#    , "level=-1", "vui.sar_idc=1", "vui.sar_height=1", "vui.sar_width=1", "vui.color_primaries=1", "vui.transfer_characteristics=1", "vui.matrix_coeffs=1", "MaxRefFrames=5", "MinIdr=60", "MaxIdr=600", "i_scenecut_threshold=40"
#    , "MaxBFrame=5", "i_bframe_adaptive=2", "i_bframe_bias=0", "i_bframe_pyramid=1", "b_deblocking_filter=True", "b_open_gop=False", "interlaced_mode=0", "constrained_intra=False", "b_intra=True", "lookahead=40"
#    , "weighted_pred=2", "weighted_bipred=True", "rect_inter=False", "amp_inter=False", "limit_modes=False", "cb_chroma_offset=0", "cr_chroma_offset=0", "me_method=3", "me_range=32", "subpel_refine=6", "limit_refs=3"
#    , "rd_level=1", "psy_rd=0.400000", "rdoq_level=0", "psy_rdoq=0.000000", "fast_pskip=True", "dct_decimate=True", "noise_reduction_intra=0", "noise_reduction_inter=0", "strong_intra_smoothing=False", "ratecontrol.rc_method=0"
#    , "ratecontrol.qp_constant=0", "ratecontrol.qp_step=4", "ratecontrol.bitrate=0", "ratecontrol.vbv_max_bitrate=0", "ratecontrol.vbv_buffer_size=0", "ratecontrol.vbv_buffer_init=1", "ratecontrol.ip_factor=1.400000"
#    , "ratecontrol.pb_factor=1.300000", "ratecontrol.aq_mode=2", "ratecontrol.aq_strength=0.600000", "ratecontrol.cu_tree=True", "ratecontrol.strict_cbr=False")
# ---------------------------------------------------
# Replace muxer name and configuration below if desired so.
# In this case, please adjust the filename extension (ext).
adm.setContainer("MKV", "forceAspectRatio=False", "displayWidth=1280", "displayAspectRatio=2", "addColourInfo=False", "colMatrixCoeff=2", "colRange=0", "colTransfer=2", "colPrimaries=2")
ext = "mkv"

Counter = 0
mark1 = 0
mark2 = 0

nbSeg = ed.nbSegments()

if not nbSeg:
    gui.displayError("Error", "No video loaded, nothing to do, bye")
    return

if nbSeg > 100:
    gui.displayInfo("Warning", "Maximum of 100 segments supported, but got " + str(nbSeg))
    nbSeg = 100

filename = ed.getRefVideoName(0)
if filename is None:
    gui.displayError("Error", "Cannot obtain reference video filename")
    return

filename = (splitext(filename))[0]
filename = basename(filename)

if filename is None:
    gui.displayError("Error", "Cannot obtain input basename")
    return

# Replace gui.dirSelect() below with output directory path for unattended operation.
outdir = gui.dirSelect("Select output folder")
if outdir is None:
    gui.displayInfo("Warning", "No output folder selected, cannot proceed")
    return

leadingZero = ""

for segmentIdx in range(nbSeg):
    mark2 += ed.getDurationForSegment(segmentIdx)
    if segmentIdx < 10:
        leadingZero = "0"
    adm.markerA = mark1
    adm.markerB = mark2
    Counter += adm.save(outdir + "/" + filename + "-segment-" + leadingZero + str(segmentIdx) + "." + ext)
    mark1 = mark2

gui.displayInfo("Finished", str(Counter) + " files out of " + str(nbSeg) + " segments converted")