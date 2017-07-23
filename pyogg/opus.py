import ctypes
import ctypes.util

from .ogg import *

try:
    libopus = ctypes.CDLL("libopus.dll")
    libopusfile = ctypes.CDLL("libopusfile.dll")
except:
    libopus = None
    libopusfile = None

if not libopus:
    PYOGG_OPUS_AVAIL = False
else:
    PYOGG_OPUS_AVAIL = True
    
if not libopusfile:
    PYOGG_OPUS_FILE_AVAIL = False
else:
    PYOGG_OPUS_FILE_AVAIL = True

# opus_types

opus_int16 = c_int16
opus_int16_p = POINTER(c_int16)
opus_uint16 = c_uint16
opus_int32 = c_int32
opus_uint32 = c_uint32

opus_int  =  c_int  
opus_int64=  c_longlong
opus_int8=    c_int8

opus_uint= c_uint
opus_uint64 = c_ulonglong
opus_uint8 = c_int8

# /opus_types

# opus_defines

"""* No error @hideinitializer"""
OPUS_OK                =0
"""* One or more invalid/out of range arguments @hideinitializer"""
OPUS_BAD_ARG          =-1
"""* Not enough bytes allocated in the buffer @hideinitializer"""
OPUS_BUFFER_TOO_SMALL =-2
"""* An internal error was detected @hideinitializer"""
OPUS_INTERNAL_ERROR   =-3
"""* The compressed data passed is corrupted @hideinitializer"""
OPUS_INVALID_PACKET   =-4
"""* Invalid/unsupported request number @hideinitializer"""
OPUS_UNIMPLEMENTED    =-5
"""* An encoder or decoder structure is invalid or already freed @hideinitializer"""
OPUS_INVALID_STATE    =-6
"""* Memory allocation has failed @hideinitializer"""
OPUS_ALLOC_FAIL       =-7

"""* These are the actual Encoder CTL ID numbers.
  * They should not be used directly by applications.
  * In general, SETs should be even and GETs should be odd."""
OPUS_SET_APPLICATION_REQUEST         =4000
OPUS_GET_APPLICATION_REQUEST         =4001
OPUS_SET_BITRATE_REQUEST             =4002
OPUS_GET_BITRATE_REQUEST             =4003
OPUS_SET_MAX_BANDWIDTH_REQUEST       =4004
OPUS_GET_MAX_BANDWIDTH_REQUEST       =4005
OPUS_SET_VBR_REQUEST                 =4006
OPUS_GET_VBR_REQUEST                 =4007
OPUS_SET_BANDWIDTH_REQUEST           =4008
OPUS_GET_BANDWIDTH_REQUEST           =4009
OPUS_SET_COMPLEXITY_REQUEST          =4010
OPUS_GET_COMPLEXITY_REQUEST          =4011
OPUS_SET_INBAND_FEC_REQUEST          =4012
OPUS_GET_INBAND_FEC_REQUEST          =4013
OPUS_SET_PACKET_LOSS_PERC_REQUEST    =4014
OPUS_GET_PACKET_LOSS_PERC_REQUEST    =4015
OPUS_SET_DTX_REQUEST                 =4016
OPUS_GET_DTX_REQUEST                 =4017
OPUS_SET_VBR_CONSTRAINT_REQUEST      =4020
OPUS_GET_VBR_CONSTRAINT_REQUEST      =4021
OPUS_SET_FORCE_CHANNELS_REQUEST      =4022
OPUS_GET_FORCE_CHANNELS_REQUEST      =4023
OPUS_SET_SIGNAL_REQUEST              =4024
OPUS_GET_SIGNAL_REQUEST              =4025
OPUS_GET_LOOKAHEAD_REQUEST           =4027
""" OPUS_RESET_STATE 4028 """
OPUS_GET_SAMPLE_RATE_REQUEST         =4029
OPUS_GET_FINAL_RANGE_REQUEST         =4031
OPUS_GET_PITCH_REQUEST               =4033
OPUS_SET_GAIN_REQUEST                =4034
OPUS_GET_GAIN_REQUEST                =4045
OPUS_SET_LSB_DEPTH_REQUEST           =4036
OPUS_GET_LSB_DEPTH_REQUEST           =4037
OPUS_GET_LAoe_pACKET_DURATION_REQUEST =4039
OPUS_SET_EXPERT_FRAME_DURATION_REQUEST =4040
OPUS_GET_EXPERT_FRAME_DURATION_REQUEST =4041
OPUS_SET_PREDICTION_DISABLED_REQUEST =4042
OPUS_GET_PREDICTION_DISABLED_REQUEST =4043
""" Don't use 4045, it's already taken by OPUS_GET_GAIN_REQUEST """
OPUS_SET_PHASE_INVERSION_DISABLED_REQUEST =4046
OPUS_GET_PHASE_INVERSION_DISABLED_REQUEST =4047

##""" Macros to trigger compilation errors when the wrong types are provided to a CTL """
##__opus_check_int(x) (((void)((x) == (opus_int32)0)), (opus_int32)(x))
##__opus_check_int_ptr(ptr) ((ptr) + ((ptr) - (opus_int32*)(ptr)))
##__opus_check_uint_ptr(ptr) ((ptr) + ((ptr) - (opus_uint32*)(ptr)))
##__opus_check_val16_ptr(ptr) ((ptr) + ((ptr) - (opus_val16*)(ptr)))
##"""* @endcond """

""" Values for the various encoder CTLs """
OPUS_AUTO                           =-1000
OPUS_BITRATE_MAX                     =  -1

"""* Best for most VoIP/videoconference applications where listening quality and intelligibility matter most
 * @hideinitializer """
OPUS_APPLICATION_VOIP               = 2048
"""* Best for broadcast/high-fidelity application where the decoded audio should be as close as possible to the input
 * @hideinitializer """
OPUS_APPLICATION_AUDIO              = 2049
"""* Only use when lowest-achievable latency is what matters most. Voice-optimized modes cannot be used.
 * @hideinitializer """
OPUS_APPLICATION_RESTRICTED_LOWDELAY =2051

OPUS_SIGNAL_VOICE                    =3001
OPUS_SIGNAL_MUSIC                    =3002 
OPUS_BANDWIDTH_NARROWBAND            =1101 
OPUS_BANDWIDTH_MEDIUMBAND            =1102 
OPUS_BANDWIDTH_WIDEBAND              =1103 
OPUS_BANDWIDTH_SUPERWIDEBAND         =1104 
OPUS_BANDWIDTH_FULLBAND              =1105 

OPUS_FRAMESIZE_ARG                   =5000 
OPUS_FRAMESIZE_2_5_MS                =5001 
OPUS_FRAMESIZE_5_MS                  =5002 
OPUS_FRAMESIZE_10_MS                 =5003
OPUS_FRAMESIZE_20_MS                 =5004 
OPUS_FRAMESIZE_40_MS                 =5005 
OPUS_FRAMESIZE_60_MS                 =5006 
OPUS_FRAMESIZE_80_MS                 =5007 
OPUS_FRAMESIZE_100_MS                =5008 
OPUS_FRAMESIZE_120_MS                =5009

##OPUS_SET_COMPLEXITY(x) OPUS_SET_COMPLEXITY_REQUEST, __opus_check_int(x)
##"""* Gets the encoder's complexity configuration.
##  * @see OPUS_SET_COMPLEXITY
##  * @param[out] x <tt>opus_int32 *</tt>: Returns a value in the range 0-10,
##  *                                      inclusive.
##  * @hideinitializer """
##OPUS_GET_COMPLEXITY(x) OPUS_GET_COMPLEXITY_REQUEST, __opus_check_int_ptr(x)
##
##"""* Configures the bitrate in the encoder.
##  * Rates from 500 to 512000 bits per second are meaningful, as well as the
##  * special values #OPUS_AUTO and #OPUS_BITRATE_MAX.
##  * The value #OPUS_BITRATE_MAX can be used to cause the codec to use as much
##  * rate as it can, which is useful for controlling the rate by adjusting the
##  * output buffer size.
##  * @see OPUS_GET_BITRATE
##  * @param[in] x <tt>opus_int32</tt>: Bitrate in bits per second. The default
##  *                                   is determined based on the number of
##  *                                   channels and the input sampling rate.
##  * @hideinitializer """
##OPUS_SET_BITRATE(x) OPUS_SET_BITRATE_REQUEST, __opus_check_int(x)
##"""* Gets the encoder's bitrate configuration.
##  * @see OPUS_SET_BITRATE
##  * @param[out] x <tt>opus_int32 *</tt>: Returns the bitrate in bits per second.
##  *                                      The default is determined based on the
##  *                                      number of channels and the input
##  *                                      sampling rate.
##  * @hideinitializer """
##OPUS_GET_BITRATE(x) OPUS_GET_BITRATE_REQUEST, __opus_check_int_ptr(x)
##
##"""* Enables or disables variable bitrate (VBR) in the encoder.
##  * The configured bitrate may not be met exactly because frames must
##  * be an integer number of bytes in length.
##  * @see OPUS_GET_VBR
##  * @see OPUS_SET_VBR_CONSTRAINT
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>0</dt><dd>Hard CBR. For LPC/hybrid modes at very low bit-rate, this can
##  *               cause noticeable quality degradation.</dd>
##  * <dt>1</dt><dd>VBR (default). The exact type of VBR is controlled by
##  *               #OPUS_SET_VBR_CONSTRAINT.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_VBR(x) OPUS_SET_VBR_REQUEST, __opus_check_int(x)
##"""* Determine if variable bitrate (VBR) is enabled in the encoder.
##  * @see OPUS_SET_VBR
##  * @see OPUS_GET_VBR_CONSTRAINT
##  * @param[out] x <tt>opus_int32 *</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>0</dt><dd>Hard CBR.</dd>
##  * <dt>1</dt><dd>VBR (default). The exact type of VBR may be retrieved via
##  *               #OPUS_GET_VBR_CONSTRAINT.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_VBR(x) OPUS_GET_VBR_REQUEST, __opus_check_int_ptr(x)
##
##"""* Enables or disables constrained VBR in the encoder.
##  * This setting is ignored when the encoder is in CBR mode.
##  * @warning Only the MDCT mode of Opus currently heeds the constraint.
##  *  Speech mode ignores it completely, hybrid mode may fail to obey it
##  *  if the LPC layer uses more bitrate than the constraint would have
##  *  permitted.
##  * @see OPUS_GET_VBR_CONSTRAINT
##  * @see OPUS_SET_VBR
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>0</dt><dd>Unconstrained VBR.</dd>
##  * <dt>1</dt><dd>Constrained VBR (default). This creates a maximum of one
##  *               frame of buffering delay assuming a transport with a
##  *               serialization speed of the nominal bitrate.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_VBR_CONSTRAINT(x) OPUS_SET_VBR_CONSTRAINT_REQUEST, __opus_check_int(x)
##"""* Determine if constrained VBR is enabled in the encoder.
##  * @see OPUS_SET_VBR_CONSTRAINT
##  * @see OPUS_GET_VBR
##  * @param[out] x <tt>opus_int32 *</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>0</dt><dd>Unconstrained VBR.</dd>
##  * <dt>1</dt><dd>Constrained VBR (default).</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_VBR_CONSTRAINT(x) OPUS_GET_VBR_CONSTRAINT_REQUEST, __opus_check_int_ptr(x)
##
##"""* Configures mono/stereo forcing in the encoder.
##  * This can force the encoder to produce packets encoded as either mono or
##  * stereo, regardless of the format of the input audio. This is useful when
##  * the caller knows that the input signal is currently a mono source embedded
##  * in a stereo stream.
##  * @see OPUS_GET_FORCE_CHANNELS
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>#OPUS_AUTO</dt><dd>Not forced (default)</dd>
##  * <dt>1</dt>         <dd>Forced mono</dd>
##  * <dt>2</dt>         <dd>Forced stereo</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_FORCE_CHANNELS(x) OPUS_SET_FORCE_CHANNELS_REQUEST, __opus_check_int(x)
##"""* Gets the encoder's forced channel configuration.
##  * @see OPUS_SET_FORCE_CHANNELS
##  * @param[out] x <tt>opus_int32 *</tt>:
##  * <dl>
##  * <dt>#OPUS_AUTO</dt><dd>Not forced (default)</dd>
##  * <dt>1</dt>         <dd>Forced mono</dd>
##  * <dt>2</dt>         <dd>Forced stereo</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_FORCE_CHANNELS(x) OPUS_GET_FORCE_CHANNELS_REQUEST, __opus_check_int_ptr(x)
##
##"""* Configures the maximum bandpass that the encoder will select automatically.
##  * Applications should normally use this instead of #OPUS_SET_BANDWIDTH
##  * (leaving that set to the default, #OPUS_AUTO). This allows the
##  * application to set an upper bound based on the type of input it is
##  * providing, but still gives the encoder the freedom to reduce the bandpass
##  * when the bitrate becomes too low, for better overall quality.
##  * @see OPUS_GET_MAX_BANDWIDTH
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>OPUS_BANDWIDTH_NARROWBAND</dt>    <dd>4 kHz passband</dd>
##  * <dt>OPUS_BANDWIDTH_MEDIUMBAND</dt>    <dd>6 kHz passband</dd>
##  * <dt>OPUS_BANDWIDTH_WIDEBAND</dt>      <dd>8 kHz passband</dd>
##  * <dt>OPUS_BANDWIDTH_SUPERWIDEBAND</dt><dd>12 kHz passband</dd>
##  * <dt>OPUS_BANDWIDTH_FULLBAND</dt>     <dd>20 kHz passband (default)</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_MAX_BANDWIDTH(x) OPUS_SET_MAX_BANDWIDTH_REQUEST, __opus_check_int(x)
##
##"""* Gets the encoder's configured maximum allowed bandpass.
##  * @see OPUS_SET_MAX_BANDWIDTH
##  * @param[out] x <tt>opus_int32 *</tt>: Allowed values:
##  * <dl>
##  * <dt>#OPUS_BANDWIDTH_NARROWBAND</dt>    <dd>4 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_MEDIUMBAND</dt>    <dd>6 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_WIDEBAND</dt>      <dd>8 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_SUPERWIDEBAND</dt><dd>12 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_FULLBAND</dt>     <dd>20 kHz passband (default)</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_MAX_BANDWIDTH(x) OPUS_GET_MAX_BANDWIDTH_REQUEST, __opus_check_int_ptr(x)
##
##"""* Sets the encoder's bandpass to a specific value.
##  * This prevents the encoder from automatically selecting the bandpass based
##  * on the available bitrate. If an application knows the bandpass of the input
##  * audio it is providing, it should normally use #OPUS_SET_MAX_BANDWIDTH
##  * instead, which still gives the encoder the freedom to reduce the bandpass
##  * when the bitrate becomes too low, for better overall quality.
##  * @see OPUS_GET_BANDWIDTH
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>#OPUS_AUTO</dt>                    <dd>(default)</dd>
##  * <dt>#OPUS_BANDWIDTH_NARROWBAND</dt>    <dd>4 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_MEDIUMBAND</dt>    <dd>6 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_WIDEBAND</dt>      <dd>8 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_SUPERWIDEBAND</dt><dd>12 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_FULLBAND</dt>     <dd>20 kHz passband</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_BANDWIDTH(x) OPUS_SET_BANDWIDTH_REQUEST, __opus_check_int(x)
##
##"""* Configures the type of signal being encoded.
##  * This is a hint which helps the encoder's mode selection.
##  * @see OPUS_GET_SIGNAL
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>#OPUS_AUTO</dt>        <dd>(default)</dd>
##  * <dt>#OPUS_SIGNAL_VOICE</dt><dd>Bias thresholds towards choosing LPC or Hybrid modes.</dd>
##  * <dt>#OPUS_SIGNAL_MUSIC</dt><dd>Bias thresholds towards choosing MDCT modes.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_SIGNAL(x) OPUS_SET_SIGNAL_REQUEST, __opus_check_int(x)
##"""* Gets the encoder's configured signal type.
##  * @see OPUS_SET_SIGNAL
##  * @param[out] x <tt>opus_int32 *</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>#OPUS_AUTO</dt>        <dd>(default)</dd>
##  * <dt>#OPUS_SIGNAL_VOICE</dt><dd>Bias thresholds towards choosing LPC or Hybrid modes.</dd>
##  * <dt>#OPUS_SIGNAL_MUSIC</dt><dd>Bias thresholds towards choosing MDCT modes.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_SIGNAL(x) OPUS_GET_SIGNAL_REQUEST, __opus_check_int_ptr(x)
##
##
##"""* Configures the encoder's intended application.
##  * The initial value is a mandatory argument to the encoder_create function.
##  * @see OPUS_GET_APPLICATION
##  * @param[in] x <tt>opus_int32</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>#OPUS_APPLICATION_VOIP</dt>
##  * <dd>Process signal for improved speech intelligibility.</dd>
##  * <dt>#OPUS_APPLICATION_AUDIO</dt>
##  * <dd>Favor faithfulness to the original input.</dd>
##  * <dt>#OPUS_APPLICATION_RESTRICTED_LOWDELAY</dt>
##  * <dd>Configure the minimum possible coding delay by disabling certain modes
##  * of operation.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_APPLICATION(x) OPUS_SET_APPLICATION_REQUEST, __opus_check_int(x)
##"""* Gets the encoder's configured application.
##  * @see OPUS_SET_APPLICATION
##  * @param[out] x <tt>opus_int32 *</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>#OPUS_APPLICATION_VOIP</dt>
##  * <dd>Process signal for improved speech intelligibility.</dd>
##  * <dt>#OPUS_APPLICATION_AUDIO</dt>
##  * <dd>Favor faithfulness to the original input.</dd>
##  * <dt>#OPUS_APPLICATION_RESTRICTED_LOWDELAY</dt>
##  * <dd>Configure the minimum possible coding delay by disabling certain modes
##  * of operation.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_APPLICATION(x) OPUS_GET_APPLICATION_REQUEST, __opus_check_int_ptr(x)
##
##"""* Gets the total samples of delay added by the entire codec.
##  * This can be queried by the encoder and then the provided number of samples can be
##  * skipped on from the start of the decoder's output to provide time aligned input
##  * and output. From the perspective of a decoding application the real data begins this many
##  * samples late.
##  *
##  * The decoder contribution to this delay is identical for all decoders, but the
##  * encoder portion of the delay may vary from implementation to implementation,
##  * version to version, or even depend on the encoder's initial configuration.
##  * Applications needing delay compensation should call this CTL rather than
##  * hard-coding a value.
##  * @param[out] x <tt>opus_int32 *</tt>:   Number of lookahead samples
##  * @hideinitializer """
##OPUS_GET_LOOKAHEAD(x) OPUS_GET_LOOKAHEAD_REQUEST, __opus_check_int_ptr(x)
##
##"""* Configures the encoder's use of inband forward error correction (FEC).
##  * @note This is only applicable to the LPC layer
##  * @see OPUS_GET_INBAND_FEC
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>0</dt><dd>Disable inband FEC (default).</dd>
##  * <dt>1</dt><dd>Enable inband FEC.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_INBAND_FEC(x) OPUS_SET_INBAND_FEC_REQUEST, __opus_check_int(x)
##"""* Gets encoder's configured use of inband forward error correction.
##  * @see OPUS_SET_INBAND_FEC
##  * @param[out] x <tt>opus_int32 *</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>0</dt><dd>Inband FEC disabled (default).</dd>
##  * <dt>1</dt><dd>Inband FEC enabled.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_INBAND_FEC(x) OPUS_GET_INBAND_FEC_REQUEST, __opus_check_int_ptr(x)
##
##"""* Configures the encoder's expected packet loss percentage.
##  * Higher values trigger progressively more loss resistant behavior in the encoder
##  * at the expense of quality at a given bitrate in the absence of packet loss, but
##  * greater quality under loss.
##  * @see OPUS_GET_PACKET_LOSS_PERC
##  * @param[in] x <tt>opus_int32</tt>:   Loss percentage in the range 0-100, inclusive (default: 0).
##  * @hideinitializer """
##OPUS_SET_PACKET_LOSS_PERC(x) OPUS_SET_PACKET_LOSS_PERC_REQUEST, __opus_check_int(x)
##"""* Gets the encoder's configured packet loss percentage.
##  * @see OPUS_SET_PACKET_LOSS_PERC
##  * @param[out] x <tt>opus_int32 *</tt>: Returns the configured loss percentage
##  *                                      in the range 0-100, inclusive (default: 0).
##  * @hideinitializer """
##OPUS_GET_PACKET_LOSS_PERC(x) OPUS_GET_PACKET_LOSS_PERC_REQUEST, __opus_check_int_ptr(x)
##
##"""* Configures the encoder's use of discontinuous transmission (DTX).
##  * @note This is only applicable to the LPC layer
##  * @see OPUS_GET_DTX
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>0</dt><dd>Disable DTX (default).</dd>
##  * <dt>1</dt><dd>Enabled DTX.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_DTX(x) OPUS_SET_DTX_REQUEST, __opus_check_int(x)
##"""* Gets encoder's configured use of discontinuous transmission.
##  * @see OPUS_SET_DTX
##  * @param[out] x <tt>opus_int32 *</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>0</dt><dd>DTX disabled (default).</dd>
##  * <dt>1</dt><dd>DTX enabled.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_DTX(x) OPUS_GET_DTX_REQUEST, __opus_check_int_ptr(x)
##"""* Configures the depth of signal being encoded.
##  *
##  * This is a hint which helps the encoder identify silence and near-silence.
##  * It represents the number of significant bits of linear intensity below
##  * which the signal contains ignorable quantization or other noise.
##  *
##  * For example, OPUS_SET_LSB_DEPTH(14) would be an appropriate setting
##  * for G.711 u-law input. OPUS_SET_LSB_DEPTH(16) would be appropriate
##  * for 16-bit linear pcm input with opus_encode_float().
##  *
##  * When using opus_encode() instead of opus_encode_float(), or when libopus
##  * is compiled for fixed-point, the encoder uses the minimum of the value
##  * set here and the value 16.
##  *
##  * @see OPUS_GET_LSB_DEPTH
##  * @param[in] x <tt>opus_int32</tt>: Input precision in bits, between 8 and 24
##  *                                   (default: 24).
##  * @hideinitializer """
##OPUS_SET_LSB_DEPTH(x) OPUS_SET_LSB_DEPTH_REQUEST, __opus_check_int(x)
##"""* Gets the encoder's configured signal depth.
##  * @see OPUS_SET_LSB_DEPTH
##  * @param[out] x <tt>opus_int32 *</tt>: Input precision in bits, between 8 and
##  *                                      24 (default: 24).
##  * @hideinitializer """
##OPUS_GET_LSB_DEPTH(x) OPUS_GET_LSB_DEPTH_REQUEST, __opus_check_int_ptr(x)
##
##"""* Configures the encoder's use of variable duration frames.
##  * When variable duration is enabled, the encoder is free to use a shorter frame
##  * size than the one requested in the opus_encode*() call.
##  * It is then the user's responsibility
##  * to verify how much audio was encoded by checking the ToC byte of the encoded
##  * packet. The part of the audio that was not encoded needs to be resent to the
##  * encoder for the next call. Do not use this option unless you <b>really</b>
##  * know what you are doing.
##  * @see OPUS_GET_EXPERT_FRAME_DURATION
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>OPUS_FRAMESIZE_ARG</dt><dd>Select frame size from the argument (default).</dd>
##  * <dt>OPUS_FRAMESIZE_2_5_MS</dt><dd>Use 2.5 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_5_MS</dt><dd>Use 5 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_10_MS</dt><dd>Use 10 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_20_MS</dt><dd>Use 20 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_40_MS</dt><dd>Use 40 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_60_MS</dt><dd>Use 60 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_80_MS</dt><dd>Use 80 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_100_MS</dt><dd>Use 100 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_120_MS</dt><dd>Use 120 ms frames.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_EXPERT_FRAME_DURATION(x) OPUS_SET_EXPERT_FRAME_DURATION_REQUEST, __opus_check_int(x)
##"""* Gets the encoder's configured use of variable duration frames.
##  * @see OPUS_SET_EXPERT_FRAME_DURATION
##  * @param[out] x <tt>opus_int32 *</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>OPUS_FRAMESIZE_ARG</dt><dd>Select frame size from the argument (default).</dd>
##  * <dt>OPUS_FRAMESIZE_2_5_MS</dt><dd>Use 2.5 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_5_MS</dt><dd>Use 5 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_10_MS</dt><dd>Use 10 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_20_MS</dt><dd>Use 20 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_40_MS</dt><dd>Use 40 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_60_MS</dt><dd>Use 60 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_80_MS</dt><dd>Use 80 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_100_MS</dt><dd>Use 100 ms frames.</dd>
##  * <dt>OPUS_FRAMESIZE_120_MS</dt><dd>Use 120 ms frames.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_EXPERT_FRAME_DURATION(x) OPUS_GET_EXPERT_FRAME_DURATION_REQUEST, __opus_check_int_ptr(x)
##
##"""* If set to 1, disables almost all use of prediction, making frames almost
##  * completely independent. This reduces quality.
##  * @see OPUS_GET_PREDICTION_DISABLED
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>0</dt><dd>Enable prediction (default).</dd>
##  * <dt>1</dt><dd>Disable prediction.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_PREDICTION_DISABLED(x) OPUS_SET_PREDICTION_DISABLED_REQUEST, __opus_check_int(x)
##"""* Gets the encoder's configured prediction status.
##  * @see OPUS_SET_PREDICTION_DISABLED
##  * @param[out] x <tt>opus_int32 *</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>0</dt><dd>Prediction enabled (default).</dd>
##  * <dt>1</dt><dd>Prediction disabled.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_PREDICTION_DISABLED(x) OPUS_GET_PREDICTION_DISABLED_REQUEST, __opus_check_int_ptr(x)
##
##"""*@}"""
##
##"""* @defgroup opus_genericctls Generic CTLs
##  *
##  * These macros are used with the \c opus_decoder_ctl and
##  * \c opus_encoder_ctl calls to generate a particular
##  * request.
##  *
##  * When called on an \c OpusDecoder they apply to that
##  * particular decoder instance. When called on an
##  * \c OpusEncoder they apply to the corresponding setting
##  * on that encoder instance, if present.
##  *
##  * Some usage examples:
##  *
##  * @code
##  * int ret;
##  * opus_int32 pitch;
##  * ret = opus_decoder_ctl(dec_ctx, OPUS_GET_PITCH(&pitch));
##  * if (ret == OPUS_OK) return ret;
##  *
##  * opus_encoder_ctl(enc_ctx, OPUS_RESET_STATE);
##  * opus_decoder_ctl(dec_ctx, OPUS_RESET_STATE);
##  *
##  * opus_int32 enc_bw, dec_bw;
##  * opus_encoder_ctl(enc_ctx, OPUS_GET_BANDWIDTH(&enc_bw));
##  * opus_decoder_ctl(dec_ctx, OPUS_GET_BANDWIDTH(&dec_bw));
##  * if (enc_bw != dec_bw) {
##  *   printf("packet bandwidth mismatch!\n");
##  * }
##  * @endcode
##  *
##  * @see opus_encoder, opus_decoder_ctl, opus_encoder_ctl, opus_decoderctls, opus_encoderctls
##  * @{
##  """

"""* Resets the codec state to be equivalent to a freshly initialized state.
  * This should be called when switching streams in order to prevent
  * the back to back decoding from giving different results from
  * one at a time decoding.
  * @hideinitializer """
OPUS_RESET_STATE =4028

##"""* Gets the final state of the codec's entropy coder.
##  * This is used for testing purposes,
##  * The encoder and decoder state should be identical after coding a payload
##  * (assuming no data corruption or software bugs)
##  *
##  * @param[out] x <tt>opus_uint32 *</tt>: Entropy coder state
##  *
##  * @hideinitializer """
##OPUS_GET_FINAL_RANGE(x) OPUS_GET_FINAL_RANGE_REQUEST, __opus_check_uint_ptr(x)
##
##"""* Gets the encoder's configured bandpass or the decoder's last bandpass.
##  * @see OPUS_SET_BANDWIDTH
##  * @param[out] x <tt>opus_int32 *</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>#OPUS_AUTO</dt>                    <dd>(default)</dd>
##  * <dt>#OPUS_BANDWIDTH_NARROWBAND</dt>    <dd>4 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_MEDIUMBAND</dt>    <dd>6 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_WIDEBAND</dt>      <dd>8 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_SUPERWIDEBAND</dt><dd>12 kHz passband</dd>
##  * <dt>#OPUS_BANDWIDTH_FULLBAND</dt>     <dd>20 kHz passband</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_BANDWIDTH(x) OPUS_GET_BANDWIDTH_REQUEST, __opus_check_int_ptr(x)
##
##"""* Gets the sampling rate the encoder or decoder was initialized with.
##  * This simply returns the <code>Fs</code> value passed to opus_encoder_init()
##  * or opus_decoder_init().
##  * @param[out] x <tt>opus_int32 *</tt>: Sampling rate of encoder or decoder.
##  * @hideinitializer
##  """
##OPUS_GET_SAMPLE_RATE(x) OPUS_GET_SAMPLE_RATE_REQUEST, __opus_check_int_ptr(x)
##
##"""* If set to 1, disables the use of phase inversion for intensity stereo,
##  * improving the quality of mono downmixes, but slightly reducing normal
##  * stereo quality. Disabling phase inversion in the decoder does not comply
##  * with RFC 6716, although it does not cause any interoperability issue and
##  * is expected to become part of the Opus standard once RFC 6716 is updated
##  * by draft-ietf-codec-opus-update.
##  * @see OPUS_GET_PHASE_INVERSION_DISABLED
##  * @param[in] x <tt>opus_int32</tt>: Allowed values:
##  * <dl>
##  * <dt>0</dt><dd>Enable phase inversion (default).</dd>
##  * <dt>1</dt><dd>Disable phase inversion.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_SET_PHASE_INVERSION_DISABLED(x) OPUS_SET_PHASE_INVERSION_DISABLED_REQUEST, __opus_check_int(x)
##"""* Gets the encoder's configured phase inversion status.
##  * @see OPUS_SET_PHASE_INVERSION_DISABLED
##  * @param[out] x <tt>opus_int32 *</tt>: Returns one of the following values:
##  * <dl>
##  * <dt>0</dt><dd>Stereo phase inversion enabled (default).</dd>
##  * <dt>1</dt><dd>Stereo phase inversion disabled.</dd>
##  * </dl>
##  * @hideinitializer """
##OPUS_GET_PHASE_INVERSION_DISABLED(x) OPUS_GET_PHASE_INVERSION_DISABLED_REQUEST, __opus_check_int_ptr(x)
##
##"""*@}"""
##
##"""* @defgroup opus_decoderctls Decoder related CTLs
##  * @see opus_genericctls, opus_encoderctls, opus_decoder
##  * @{
##  """
##
##"""* Configures decoder gain adjustment.
##  * Scales the decoded output by a factor specified in Q8 dB units.
##  * This has a maximum range of -32768 to 32767 inclusive, and returns
##  * OPUS_BAD_ARG otherwise. The default is zero indicating no adjustment.
##  * This setting survives decoder reset.
##  *
##  * gain = pow(10, x/(20.0*256))
##  *
##  * @param[in] x <tt>opus_int32</tt>:   Amount to scale PCM signal by in Q8 dB units.
##  * @hideinitializer """
##OPUS_SET_GAIN(x) OPUS_SET_GAIN_REQUEST, __opus_check_int(x)
##"""* Gets the decoder's configured gain adjustment. @see OPUS_SET_GAIN
##  *
##  * @param[out] x <tt>opus_int32 *</tt>: Amount to scale PCM signal by in Q8 dB units.
##  * @hideinitializer """
##OPUS_GET_GAIN(x) OPUS_GET_GAIN_REQUEST, __opus_check_int_ptr(x)
##
##"""* Gets the duration (in samples) of the last packet successfully decoded or concealed.
##  * @param[out] x <tt>opus_int32 *</tt>: Number of samples (at current sampling rate).
##  * @hideinitializer """
##OPUS_GET_LAoe_pACKET_DURATION(x) OPUS_GET_LAoe_pACKET_DURATION_REQUEST, __opus_check_int_ptr(x)
##
##"""* Gets the pitch of the last decoded frame, if available.
##  * This can be used for any post-processing algorithm requiring the use of pitch,
##  * e.g. time stretching/shortening. If the last frame was not voiced, or if the
##  * pitch was not coded in the frame, then zero is returned.
##  *
##  * This CTL is only implemented for decoder instances.
##  *
##  * @param[out] x <tt>opus_int32 *</tt>: pitch period at 48 kHz (or 0 if not available)
##  *
##  * @hideinitializer """
##OPUS_GET_PITCH(x) OPUS_GET_PITCH_REQUEST, __opus_check_int_ptr(x)
##
##"""*@}"""
##
##"""* @defgroup opus_libinfo Opus library information functions
##  * @{
##  """
##
##"""* Converts an opus error code into a human readable string.
##  *
##  * @param[in] error <tt>int</tt>: Error number
##  * @returns Error string
##  """
##OPUS_EXPORT const char *opus_strerror(int error);
##
##"""* Gets the libopus version string.
##  *
##  * Applications may look for the substring "-fixed" in the version string to
##  * determine whether they have a fixed-point or floating-point build at
##  * runtime.
##  *
##  * @returns Version string
##  """
##OPUS_EXPORT const char *opus_get_version_string(void);
  
# /opus_defines

# opus


"""* Opus encoder state.
  * This contains the complete state of an Opus encoder.
  * It is position independent and can be freely copied.
  * @see opus_encoder_create,opus_encoder_init
  """
##typedef struct OpusEncoder OpusEncoder;
class OpusEncoder(ctypes.Structure):
    _fields_ = [("dummy", ctypes.c_int)]

oe_p = POINTER(OpusEncoder)

"""* Gets the size of an <code>OpusEncoder</code> structure.
  * @param[in] channels <tt>int</tt>: Number of channels.
  *                                   This must be 1 or 2.
  * @returns The size in bytes.
  """
libopus.opus_encoder_get_size.restype = c_int
libopus.opus_encoder_get_size.argtypes = [c_int]

def opus_encoder_get_size(channels):
    return libopus.opus_encoder_get_size(channels)

"""*
 """

"""* Allocates and initializes an encoder state.
 * There are three coding modes:
 *
 * @ref OPUS_APPLICATION_VOIP gives best quality at a given bitrate for voice
 *    signals. It enhances the  input signal by high-pass filtering and
 *    emphasizing formants and harmonics. Optionally  it includes in-band
 *    forward error correction to protect against packet loss. Use this
 *    mode for typical VoIP applications. Because of the enhancement,
 *    even at high bitrates the output may sound different from the input.
 *
 * @ref OPUS_APPLICATION_AUDIO gives best quality at a given bitrate for most
 *    non-voice signals like music. Use this mode for music and mixed
 *    (music/voice) content, broadcast, and applications requiring less
 *    than 15 ms of coding delay.
 *
 * @ref OPUS_APPLICATION_RESTRICTED_LOWDELAY configures low-delay mode that
 *    disables the speech-optimized mode in exchange for slightly reduced delay.
 *    This mode can only be set on an newly initialized or freshly reset encoder
 *    because it changes the codec delay.
 *
 * This is useful when the caller knows that the speech-optimized modes will not be needed (use with caution).
 * @param [in] Fs <tt>opus_int32</tt>: Sampling rate of input signal (Hz)
 *                                     This must be one of 8000, 12000, 16000,
 *                                     24000, or 48000.
 * @param [in] channels <tt>int</tt>: Number of channels (1 or 2) in input signal
 * @param [in] application <tt>int</tt>: Coding mode (@ref OPUS_APPLICATION_VOIP/@ref OPUS_APPLICATION_AUDIO/@ref OPUS_APPLICATION_RESTRICTED_LOWDELAY)
 * @param [out] error <tt>int*</tt>: @ref opus_errorcodes
 * @note Regardless of the sampling rate and number channels selected, the Opus encoder
 * can switch to a lower audio bandwidth or number of channels if the bitrate
 * selected is too low. This also means that it is safe to always use 48 kHz stereo input
 * and let the encoder optimize the encoding.
 """
libopus.opus_encoder_create.restype = oe_p
libopus.opus_encoder_create.argtypes = [opus_int32, c_int, c_int, c_int_p]

def opus_encoder_create(Fs, channels, application, error):
    return libopus.opus_encoder_create(Fs, channels, application, error)

"""* Initializes a previously allocated encoder state
  * The memory pointed to by st must be at least the size returned by opus_encoder_get_size().
  * This is intended for applications which use their own allocator instead of malloc.
  * @see opus_encoder_create(),opus_encoder_get_size()
  * To reset a previously initialized state, use the #OPUS_RESET_STATE CTL.
  * @param [in] st <tt>OpusEncoder*</tt>: Encoder state
  * @param [in] Fs <tt>opus_int32</tt>: Sampling rate of input signal (Hz)
 *                                      This must be one of 8000, 12000, 16000,
 *                                      24000, or 48000.
  * @param [in] channels <tt>int</tt>: Number of channels (1 or 2) in input signal
  * @param [in] application <tt>int</tt>: Coding mode (OPUS_APPLICATION_VOIP/OPUS_APPLICATION_AUDIO/OPUS_APPLICATION_RESTRICTED_LOWDELAY)
  * @retval #OPUS_OK Success or @ref opus_errorcodes
  """
libopus.opus_encoder_init.restype = c_int
libopus.opus_encoder_init.argtypes = [oe_p, opus_int32, c_int, c_int]

def opus_encoder_init(st, Fs, channels, applications):
    return libopus.opus_encoder_init(st, Fs, channels, applications)

"""* Encodes an Opus frame.
  * @param [in] st <tt>OpusEncoder*</tt>: Encoder state
  * @param [in] pcm <tt>opus_int16*</tt>: Input signal (interleaved if 2 channels). length is frame_size*channels*sizeof(opus_int16)
  * @param [in] frame_size <tt>int</tt>: Number of samples per channel in the
  *                                      input signal.
  *                                      This must be an Opus frame size for
  *                                      the encoder's sampling rate.
  *                                      For example, at 48 kHz the permitted
  *                                      values are 120, 240, 480, 960, 1920,
  *                                      and 2880.
  *                                      Passing in a duration of less than
  *                                      10 ms (480 samples at 48 kHz) will
  *                                      prevent the encoder from using the LPC
  *                                      or hybrid modes.
  * @param [out] data <tt>unsigned char*</tt>: Output payload.
  *                                            This must contain storage for at
  *                                            least \a max_data_bytes.
  * @param [in] max_data_bytes <tt>opus_int32</tt>: Size of the allocated
  *                                                 memory for the output
  *                                                 payload. This may be
  *                                                 used to impose an upper limit on
  *                                                 the instant bitrate, but should
  *                                                 not be used as the only bitrate
  *                                                 control. Use #OPUS_SET_BITRATE to
  *                                                 control the bitrate.
  * @returns The length of the encoded packet (in bytes) on success or a
  *          negative error code (see @ref opus_errorcodes) on failure.
  """
libopus.opus_encode.restype = opus_int32
libopus.opus_encode.argtypes = [oe_p, opus_int16_p, c_int, c_uchar_p, opus_int32]

def opus_encode(st, pcm, frame_size, data, max_data_bytes):
    return libopus.opus_encode(st, pcm, frame_size, data, max_data_bytes)

"""* Encodes an Opus frame from floating point input.
  * @param [in] st <tt>OpusEncoder*</tt>: Encoder state
  * @param [in] pcm <tt>float*</tt>: Input in float format (interleaved if 2 channels), with a normal range of +/-1.0.
  *          Samples with a range beyond +/-1.0 are supported but will
  *          be clipped by decoders using the integer API and should
  *          only be used if it is known that the far end supports
  *          extended dynamic range.
  *          length is frame_size*channels*sizeof(float)
  * @param [in] frame_size <tt>int</tt>: Number of samples per channel in the
  *                                      input signal.
  *                                      This must be an Opus frame size for
  *                                      the encoder's sampling rate.
  *                                      For example, at 48 kHz the permitted
  *                                      values are 120, 240, 480, 960, 1920,
  *                                      and 2880.
  *                                      Passing in a duration of less than
  *                                      10 ms (480 samples at 48 kHz) will
  *                                      prevent the encoder from using the LPC
  *                                      or hybrid modes.
  * @param [out] data <tt>unsigned char*</tt>: Output payload.
  *                                            This must contain storage for at
  *                                            least \a max_data_bytes.
  * @param [in] max_data_bytes <tt>opus_int32</tt>: Size of the allocated
  *                                                 memory for the output
  *                                                 payload. This may be
  *                                                 used to impose an upper limit on
  *                                                 the instant bitrate, but should
  *                                                 not be used as the only bitrate
  *                                                 control. Use #OPUS_SET_BITRATE to
  *                                                 control the bitrate.
  * @returns The length of the encoded packet (in bytes) on success or a
  *          negative error code (see @ref opus_errorcodes) on failure.
  """
libopus.opus_encode_float.restype = opus_int32
libopus.opus_encode_float.argtypes = [oe_p, c_float_p, c_int, c_uchar_p, opus_int32]

def opus_encode_float(st, pcm, frame_size, data, max_data_bytes):
    return libopus.opus_encode_float(st, pcm, frame_size, data, max_data_bytes)

"""* Frees an <code>OpusEncoder</code> allocated by opus_encoder_create().
  * @param[in] st <tt>OpusEncoder*</tt>: State to be freed.
  """
libopus.opus_encoder_destroy.restype = None
libopus.opus_encoder_destroy.argtypes = [oe_p]

def opus_encoder_destroy(st):
    return libopus.opus_encoder_destroy(st)

"""* Perform a CTL function on an Opus encoder.
  *
  * Generally the request and subsequent arguments are generated
  * by a convenience macro.
  * @param st <tt>OpusEncoder*</tt>: Encoder state.
  * @param request This and all remaining parameters should be replaced by one
  *                of the convenience macros in @ref opus_genericctls or
  *                @ref opus_encoderctls.
  * @see opus_genericctls
  * @see opus_encoderctls
  """
libopus.opus_encoder_ctl.restype = c_int
libopus.opus_encoder_ctl.argtypes = [oe_p, c_int]

def opus_encoder_ctl(st, request):
    return libopus.opus_encoder_ctl(st, request)
##OPUS_EXPORT int opus_encoder_ctl(OpusEncoder *st, int request, ...) OPUS_ARG_NONNULL(1);
"""*@}"""

"""* @defgroup opus_decoder Opus Decoder
  * @{
  *
  * @brief This page describes the process and functions used to decode Opus.
  *
  * The decoding process also starts with creating a decoder
  * state. This can be done with:
  * @code
  * int          error;
  * OpusDecoder *dec;
  * dec = opus_decoder_create(Fs, channels, &error);
  * @endcode
  * where
  * @li Fs is the sampling rate and must be 8000, 12000, 16000, 24000, or 48000
  * @li channels is the number of channels (1 or 2)
  * @li error will hold the error code in case of failure (or #OPUS_OK on success)
  * @li the return value is a newly created decoder state to be used for decoding
  *
  * While opus_decoder_create() allocates memory for the state, it's also possible
  * to initialize pre-allocated memory:
  * @code
  * int          size;
  * int          error;
  * OpusDecoder *dec;
  * size = opus_decoder_get_size(channels);
  * dec = malloc(size);
  * error = opus_decoder_init(dec, Fs, channels);
  * @endcode
  * where opus_decoder_get_size() returns the required size for the decoder state. Note that
  * future versions of this code may change the size, so no assuptions should be made about it.
  *
  * The decoder state is always continuous in memory and only a shallow copy is sufficient
  * to copy it (e.g. memcpy())
  *
  * To decode a frame, opus_decode() or opus_decode_float() must be called with a packet of compressed audio data:
  * @code
  * frame_size = opus_decode(dec, packet, len, decoded, max_size, 0);
  * @endcode
  * where
  *
  * @li packet is the byte array containing the compressed data
  * @li len is the exact number of bytes contained in the packet
  * @li decoded is the decoded audio data in opus_int16 (or float for opus_decode_float())
  * @li max_size is the max duration of the frame in samples (per channel) that can fit into the decoded_frame array
  *
  * opus_decode() and opus_decode_float() return the number of samples (per channel) decoded from the packet.
  * If that value is negative, then an error has occurred. This can occur if the packet is corrupted or if the audio
  * buffer is too small to hold the decoded audio.
  *
  * Opus is a stateful codec with overlapping blocks and as a result Opus
  * packets are not coded independently of each other. Packets must be
  * passed into the decoder serially and in the correct order for a correct
  * decode. Lost packets can be replaced with loss concealment by calling
  * the decoder with a null pointer and zero length for the missing packet.
  *
  * A single codec state may only be accessed from a single thread at
  * a time and any required locking must be performed by the caller. Separate
  * streams must be decoded with separate decoder states and can be decoded
  * in parallel unless the library was compiled with NONTHREADSAFE_PSEUDOSTACK
  * defined.
  *
  """

"""* Opus decoder state.
  * This contains the complete state of an Opus decoder.
  * It is position independent and can be freely copied.
  * @see opus_decoder_create,opus_decoder_init
  """
##typedef struct OpusDecoder OpusDecoder;

class OpusDecoder(ctypes.Structure):
    _fields_ = [("dummy", c_int)]

od_p = POINTER(OpusDecoder)

"""* Gets the size of an <code>OpusDecoder</code> structure.
  * @param [in] channels <tt>int</tt>: Number of channels.
  *                                    This must be 1 or 2.
  * @returns The size in bytes.
  """
libopus.opus_decoder_get_size.restype = c_int
libopus.opus_decoder_get_size.argtypes = [c_int]

def opus_decoder_get_size(channels):
    return libopus.opus_decoder_get_size(channels)
##OPUS_EXPORT OPUS_WARN_UNUSED_RESULT int opus_decoder_get_size(int channels);

"""* Allocates and initializes a decoder state.
  * @param [in] Fs <tt>opus_int32</tt>: Sample rate to decode at (Hz).
  *                                     This must be one of 8000, 12000, 16000,
  *                                     24000, or 48000.
  * @param [in] channels <tt>int</tt>: Number of channels (1 or 2) to decode
  * @param [out] error <tt>int*</tt>: #OPUS_OK Success or @ref opus_errorcodes
  *
  * Internally Opus stores data at 48000 Hz, so that should be the default
  * value for Fs. However, the decoder can efficiently decode to buffers
  * at 8, 12, 16, and 24 kHz so if for some reason the caller cannot use
  * data at the full sample rate, or knows the compressed data doesn't
  * use the full frequency range, it can request decoding at a reduced
  * rate. Likewise, the decoder is capable of filling in either mono or
  * interleaved stereo pcm buffers, at the caller's request.
  """
libopus.opus_decoder_create.restype = od_p
libopus.opus_decoder_create.argtypes = [opus_int32, c_int, c_int_p]

def opus_decoder_create(Fs, channels, error):
    return libopus.opus_decoder_create(Fs, channels, error)

"""* Initializes a previously allocated decoder state.
  * The state must be at least the size returned by opus_decoder_get_size().
  * This is intended for applications which use their own allocator instead of malloc. @see opus_decoder_create,opus_decoder_get_size
  * To reset a previously initialized state, use the #OPUS_RESET_STATE CTL.
  * @param [in] st <tt>OpusDecoder*</tt>: Decoder state.
  * @param [in] Fs <tt>opus_int32</tt>: Sampling rate to decode to (Hz).
  *                                     This must be one of 8000, 12000, 16000,
  *                                     24000, or 48000.
  * @param [in] channels <tt>int</tt>: Number of channels (1 or 2) to decode
  * @retval #OPUS_OK Success or @ref opus_errorcodes
  """
libopus.opus_decoder_init.restype = c_int
libopus.opus_decoder_init.argtypes = [od_p, opus_int32, c_int]

def opus_decoder_init(st, Fs, channels):
    return libopus.opus_decoder_init(st, Fs, channels)

"""* Decode an Opus packet.
  * @param [in] st <tt>OpusDecoder*</tt>: Decoder state
  * @param [in] data <tt>char*</tt>: Input payload. Use a NULL pointer to indicate packet loss
  * @param [in] len <tt>opus_int32</tt>: Number of bytes in payload*
  * @param [out] pcm <tt>opus_int16*</tt>: Output signal (interleaved if 2 channels). length
  *  is frame_size*channels*sizeof(opus_int16)
  * @param [in] frame_size Number of samples per channel of available space in \a pcm.
  *  If this is less than the maximum packet duration (120ms; 5760 for 48kHz), this function will
  *  not be capable of decoding some packets. In the case of PLC (data==NULL) or FEC (decode_fec=1),
  *  then frame_size needs to be exactly the duration of audio that is missing, otherwise the
  *  decoder will not be in the optimal state to decode the next incoming packet. For the PLC and
  *  FEC cases, frame_size <b>must</b> be a multiple of 2.5 ms.
  * @param [in] decode_fec <tt>int</tt>: Flag (0 or 1) to request that any in-band forward error correction data be
  *  decoded. If no such data is available, the frame is decoded as if it were lost.
  * @returns Number of decoded samples or @ref opus_errorcodes
  """
libopus.opus_decode.restype = c_int
libopus.opus_decode.argtypes = [od_p, c_uchar_p, opus_int32, opus_int16_p, c_int, c_int]

def opus_decode(st, data, len, pcm, frame_size, decode_fec):
    return libopus.opus_decode(st, data, len, pcm, frame_size, decode_fec)

"""* Decode an Opus packet with floating point output.
  * @param [in] st <tt>OpusDecoder*</tt>: Decoder state
  * @param [in] data <tt>char*</tt>: Input payload. Use a NULL pointer to indicate packet loss
  * @param [in] len <tt>opus_int32</tt>: Number of bytes in payload
  * @param [out] pcm <tt>float*</tt>: Output signal (interleaved if 2 channels). length
  *  is frame_size*channels*sizeof(float)
  * @param [in] frame_size Number of samples per channel of available space in \a pcm.
  *  If this is less than the maximum packet duration (120ms; 5760 for 48kHz), this function will
  *  not be capable of decoding some packets. In the case of PLC (data==NULL) or FEC (decode_fec=1),
  *  then frame_size needs to be exactly the duration of audio that is missing, otherwise the
  *  decoder will not be in the optimal state to decode the next incoming packet. For the PLC and
  *  FEC cases, frame_size <b>must</b> be a multiple of 2.5 ms.
  * @param [in] decode_fec <tt>int</tt>: Flag (0 or 1) to request that any in-band forward error correction data be
  *  decoded. If no such data is available the frame is decoded as if it were lost.
  * @returns Number of decoded samples or @ref opus_errorcodes
  """
libopus.opus_decode_float.restype = c_int
libopus.opus_decode_float.argtypes = [od_p, c_uchar_p, opus_int32, c_float_p, c_int, c_int]

def opus_decode_float(st, data, len, pcm, frame_size, decode_fec):
    return libopus.opus_decode_float(st, data, len, pcm, frame_size, decode_fec)

"""* Perform a CTL function on an Opus decoder.
  *
  * Generally the request and subsequent arguments are generated
  * by a convenience macro.
  * @param st <tt>OpusDecoder*</tt>: Decoder state.
  * @param request This and all remaining parameters should be replaced by one
  *                of the convenience macros in @ref opus_genericctls or
  *                @ref opus_decoderctls.
  * @see opus_genericctls
  * @see opus_decoderctls
  """
libopus.opus_decoder_ctl.restype = c_int
libopus.opus_decoder_ctl.argtypes = [od_p, c_int]

def opus_decoder_ctl(st, request):
    return libopus.opus_decoder_ctl(st, request)

"""* Frees an <code>OpusDecoder</code> allocated by opus_decoder_create().
  * @param[in] st <tt>OpusDecoder*</tt>: State to be freed.
  """
libopus.opus_decoder_destroy.restype = None
libopus.opus_decoder_destroy.argtypes = [od_p]

def opus_decoder_destroy(st):
    return libopus.opus_decoder_destroy(st)

"""* Parse an opus packet into one or more frames.
  * Opus_decode will perform this operation internally so most applications do
  * not need to use this function.
  * This function does not copy the frames, the returned pointers are pointers into
  * the input packet.
  * @param [in] data <tt>char*</tt>: Opus packet to be parsed
  * @param [in] len <tt>opus_int32</tt>: size of data
  * @param [out] out_toc <tt>char*</tt>: TOC pointer
  * @param [out] frames <tt>char*[48]</tt> encapsulated frames
  * @param [out] size <tt>opus_int16[48]</tt> sizes of the encapsulated frames
  * @param [out] payload_offset <tt>int*</tt>: returns the position of the payload within the packet (in bytes)
  * @returns number of frames
  """
libopus.opus_packet_parse.restype = c_int
libopus.opus_packet_parse.argtypes = [c_uchar_p, opus_int32, c_uchar_p, c_uchar_p*48, opus_int16*48, c_int_p]

def opus_packet_parse(data, len, out_toc, frames, size, payload_offset):
    return libopus.opus_packet_parse(data, len, out_toc, frames, size, payload_offset)

"""* Gets the bandwidth of an Opus packet.
  * @param [in] data <tt>char*</tt>: Opus packet
  * @retval OPUS_BANDWIDTH_NARROWBAND Narrowband (4kHz bandpass)
  * @retval OPUS_BANDWIDTH_MEDIUMBAND Mediumband (6kHz bandpass)
  * @retval OPUS_BANDWIDTH_WIDEBAND Wideband (8kHz bandpass)
  * @retval OPUS_BANDWIDTH_SUPERWIDEBAND Superwideband (12kHz bandpass)
  * @retval OPUS_BANDWIDTH_FULLBAND Fullband (20kHz bandpass)
  * @retval OPUS_INVALID_PACKET The compressed data passed is corrupted or of an unsupported type
  """
libopus.opus_packet_get_bandwidth.restype = c_int
libopus.opus_packet_get_bandwidth.argtypes = [c_uchar_p]

def opus_packet_get_bandwidth(data):
    return libopus.opus_packet_get_bandwidth(data)

"""* Gets the number of samples per frame from an Opus packet.
  * @param [in] data <tt>char*</tt>: Opus packet.
  *                                  This must contain at least one byte of
  *                                  data.
  * @param [in] Fs <tt>opus_int32</tt>: Sampling rate in Hz.
  *                                     This must be a multiple of 400, or
  *                                     inaccurate results will be returned.
  * @returns Number of samples per frame.
  """
libopus.opus_packet_get_samples_per_frame.restype = c_int
libopus.opus_packet_get_samples_per_frame.argtypes = [c_uchar_p, opus_int32]

def opus_packet_get_samples_per_frame(data, Fs):
    return libopus.opus_packet_get_samples_per_frame(data, Fs)

"""* Gets the number of channels from an Opus packet.
  * @param [in] data <tt>char*</tt>: Opus packet
  * @returns Number of channels
  * @retval OPUS_INVALID_PACKET The compressed data passed is corrupted or of an unsupported type
  """
libopus.opus_packet_get_nb_channels.restype = c_int
libopus.opus_packet_get_nb_channels.argtypes = [c_uchar_p]

def opus_packet_get_nb_channels(data):
    return libopus.opus_packet_get_nb_channels(data)

"""* Gets the number of frames in an Opus packet.
  * @param [in] packet <tt>char*</tt>: Opus packet
  * @param [in] len <tt>opus_int32</tt>: Length of packet
  * @returns Number of frames
  * @retval OPUS_BAD_ARG Insufficient data was passed to the function
  * @retval OPUS_INVALID_PACKET The compressed data passed is corrupted or of an unsupported type
  """
libopus.opus_packet_get_nb_frames.restype = c_int
libopus.opus_packet_get_nb_frames.argtypes = [c_uchar*0, opus_int32]

def opus_packet_get_nb_frames(packet, len):
    return libopus.opus_packet_get_nb_frames(packet, len)

"""* Gets the number of samples of an Opus packet.
  * @param [in] packet <tt>char*</tt>: Opus packet
  * @param [in] len <tt>opus_int32</tt>: Length of packet
  * @param [in] Fs <tt>opus_int32</tt>: Sampling rate in Hz.
  *                                     This must be a multiple of 400, or
  *                                     inaccurate results will be returned.
  * @returns Number of samples
  * @retval OPUS_BAD_ARG Insufficient data was passed to the function
  * @retval OPUS_INVALID_PACKET The compressed data passed is corrupted or of an unsupported type
  """
libopus.opus_packet_get_nb_samples.restype = c_int
libopus.opus_packet_get_nb_samples.argtypes = [c_uchar*0, opus_int32, opus_int32]

def opus_packet_get_nb_samples(packet, len, Fs):
    return libopus.opus_packet_get_nb_samples(packet, len, Fs)

"""* Gets the number of samples of an Opus packet.
  * @param [in] dec <tt>OpusDecoder*</tt>: Decoder state
  * @param [in] packet <tt>char*</tt>: Opus packet
  * @param [in] len <tt>opus_int32</tt>: Length of packet
  * @returns Number of samples
  * @retval OPUS_BAD_ARG Insufficient data was passed to the function
  * @retval OPUS_INVALID_PACKET The compressed data passed is corrupted or of an unsupported type
  """
libopus.opus_decoder_get_nb_samples.restype = c_int
libopus.opus_decoder_get_nb_samples.argtypes = [od_p, c_uchar*0, opus_int32]

def opus_decoder_get_nb_samples(dec, packet, len):
    return libopus.opus_decoder_get_nb_samples(dec, packet, len)

"""* Applies soft-clipping to bring a float signal within the [-1,1] range. If
  * the signal is already in that range, nothing is done. If there are values
  * outside of [-1,1], then the signal is clipped as smoothly as possible to
  * both fit in the range and avoid creating excessive distortion in the
  * process.
  * @param [in,out] pcm <tt>float*</tt>: Input PCM and modified PCM
  * @param [in] frame_size <tt>int</tt> Number of samples per channel to process
  * @param [in] channels <tt>int</tt>: Number of channels
  * @param [in,out] softclip_mem <tt>float*</tt>: State memory for the soft clipping process (one float per channel, initialized to zero)
  """
libopus.opus_pcm_soft_clip.restype = None
libopus.opus_pcm_soft_clip.argtypes = [c_float_p, c_int, c_int, c_float_p]

def opus_pcm_soft_clip(pcm, frame_size, channels, softclip_mem):
    return libopus.opus_pcm_soft_clip(pcm, frame_size, channels, softclip_mem)

"""*@}"""

"""* @defgroup opus_repacketizer Repacketizer
  * @{
  *
  * The repacketizer can be used to merge multiple Opus packets into a single
  * packet or alternatively to split Opus packets that have previously been
  * merged. Splitting valid Opus packets is always guaranteed to succeed,
  * whereas merging valid packets only succeeds if all frames have the same
  * mode, bandwidth, and frame size, and when the total duration of the merged
  * packet is no more than 120 ms. The 120 ms limit comes from the
  * specification and limits decoder memory requirements at a point where
  * framing overhead becomes negligible.
  *
  * The repacketizer currently only operates on elementary Opus
  * streams. It will not manipualte multistream packets successfully, except in
  * the degenerate case where they consist of data from a single stream.
  *
  * The repacketizing process starts with creating a repacketizer state, either
  * by calling opus_repacketizer_create() or by allocating the memory yourself,
  * e.g.,
  * @code
  * OpusRepacketizer *rp;
  * rp = (OpusRepacketizer*)malloc(opus_repacketizer_get_size());
  * if (rp != NULL)
  *     opus_repacketizer_init(rp);
  * @endcode
  *
  * Then the application should submit packets with opus_repacketizer_cat(),
  * extract new packets with opus_repacketizer_out() or
  * opus_repacketizer_out_range(), and then reset the state for the next set of
  * input packets via opus_repacketizer_init().
  *
  * For example, to split a sequence of packets into individual frames:
  * @code
  * unsigned char *data;
  * int len;
  * while (get_next_packet(&data, &len))
  * {
  *   unsigned char out[1276];
  *   opus_int32 out_len;
  *   int nb_frames;
  *   int err;
  *   int i;
  *   err = opus_repacketizer_cat(rp, data, len);
  *   if (err != OPUS_OK)
  *   {
  *     release_packet(data);
  *     return err;
  *   }
  *   nb_frames = opus_repacketizer_get_nb_frames(rp);
  *   for (i = 0; i < nb_frames; i++)
  *   {
  *     out_len = opus_repacketizer_out_range(rp, i, i+1, out, sizeof(out));
  *     if (out_len < 0)
  *     {
  *        release_packet(data);
  *        return (int)out_len;
  *     }
  *     output_next_packet(out, out_len);
  *   }
  *   opus_repacketizer_init(rp);
  *   release_packet(data);
  * }
  * @endcode
  *
  * Alternatively, to combine a sequence of frames into packets that each
  * contain up to <code>TARGET_DURATION_MS</code> milliseconds of data:
  * @code
  * // The maximum number of packets with duration TARGET_DURATION_MS occurs
  * // when the frame size is 2.5 ms, for a total of (TARGET_DURATION_MS*2/5)
  * // packets.
  * unsigned char *data[(TARGET_DURATION_MS*2/5)+1];
  * opus_int32 len[(TARGET_DURATION_MS*2/5)+1];
  * int nb_packets;
  * unsigned char out[1277*(TARGET_DURATION_MS*2/2)];
  * opus_int32 out_len;
  * int prev_toc;
  * nb_packets = 0;
  * while (get_next_packet(data+nb_packets, len+nb_packets))
  * {
  *   int nb_frames;
  *   int err;
  *   nb_frames = opus_packet_get_nb_frames(data[nb_packets], len[nb_packets]);
  *   if (nb_frames < 1)
  *   {
  *     release_packets(data, nb_packets+1);
  *     return nb_frames;
  *   }
  *   nb_frames += opus_repacketizer_get_nb_frames(rp);
  *   // If adding the next packet would exceed our target, or it has an
  *   // incompatible TOC sequence, output the packets we already have before
  *   // submitting it.
  *   // N.B., The nb_packets > 0 check ensures we've submitted at least one
  *   // packet since the last call to opus_repacketizer_init(). Otherwise a
  *   // single packet longer than TARGET_DURATION_MS would cause us to try to
  *   // output an (invalid) empty packet. It also ensures that prev_toc has
  *   // been set to a valid value. Additionally, len[nb_packets] > 0 is
  *   // guaranteed by the call to opus_packet_get_nb_frames() above, so the
  *   // reference to data[nb_packets][0] should be valid.
  *   if (nb_packets > 0 && (
  *       ((prev_toc & 0xFC) != (data[nb_packets][0] & 0xFC)) ||
  *       opus_packet_get_samples_per_frame(data[nb_packets], 48000)*nb_frames >
  *       TARGET_DURATION_MS*48))
  *   {
  *     out_len = opus_repacketizer_out(rp, out, sizeof(out));
  *     if (out_len < 0)
  *     {
  *        release_packets(data, nb_packets+1);
  *        return (int)out_len;
  *     }
  *     output_next_packet(out, out_len);
  *     opus_repacketizer_init(rp);
  *     release_packets(data, nb_packets);
  *     data[0] = data[nb_packets];
  *     len[0] = len[nb_packets];
  *     nb_packets = 0;
  *   }
  *   err = opus_repacketizer_cat(rp, data[nb_packets], len[nb_packets]);
  *   if (err != OPUS_OK)
  *   {
  *     release_packets(data, nb_packets+1);
  *     return err;
  *   }
  *   prev_toc = data[nb_packets][0];
  *   nb_packets++;
  * }
  * // Output the final, partial packet.
  * if (nb_packets > 0)
  * {
  *   out_len = opus_repacketizer_out(rp, out, sizeof(out));
  *   release_packets(data, nb_packets);
  *   if (out_len < 0)
  *     return (int)out_len;
  *   output_next_packet(out, out_len);
  * }
  * @endcode
  *
  * An alternate way of merging packets is to simply call opus_repacketizer_cat()
  * unconditionally until it fails. At that point, the merged packet can be
  * obtained with opus_repacketizer_out() and the input packet for which
  * opus_repacketizer_cat() needs to be re-added to a newly reinitialized
  * repacketizer state.
  """

##typedef struct OpusRepacketizer OpusRepacketizer;

class OpusRepacketizer(ctypes.Structure):
    _fields_ = [("dummy", c_int)]

or_p = POINTER(OpusRepacketizer)

"""* Gets the size of an <code>OpusRepacketizer</code> structure.
  * @returns The size in bytes.
  """
libopus.opus_repacketizer_get_size.restype = c_int
libopus.opus_repacketizer_get_size.argtypes = None

def opus_repacketizer_get_size():
    return libopus.opus_repacketizer_get_size()

"""* (Re)initializes a previously allocated repacketizer state.
  * The state must be at least the size returned by opus_repacketizer_get_size().
  * This can be used for applications which use their own allocator instead of
  * malloc().
  * It must also be called to reset the queue of packets waiting to be
  * repacketized, which is necessary if the maximum packet duration of 120 ms
  * is reached or if you wish to submit packets with a different Opus
  * configuration (coding mode, audio bandwidth, frame size, or channel count).
  * Failure to do so will prevent a new packet from being added with
  * opus_repacketizer_cat().
  * @see opus_repacketizer_create
  * @see opus_repacketizer_get_size
  * @see opus_repacketizer_cat
  * @param rp <tt>OpusRepacketizer*</tt>: The repacketizer state to
  *                                       (re)initialize.
  * @returns A pointer to the same repacketizer state that was passed in.
  """
libopus.opus_repacketizer_init.restype = or_p
libopus.opus_repacketizer_init.argtypes = [or_p]

def opus_repacketizer_init(rp):
    return libopus.opus_repacketizer_init(rp)

"""* Allocates memory and initializes the new repacketizer with
 * opus_repacketizer_init().
  """
libopus.opus_repacketizer_create.restype = or_p
libopus.opus_repacketizer_create.argtypes = None

def opus_repacketizer_create():
    return libopus.opus_repacketizer_create()

"""* Frees an <code>OpusRepacketizer</code> allocated by
  * opus_repacketizer_create().
  * @param[in] rp <tt>OpusRepacketizer*</tt>: State to be freed.
  """
libopus.opus_repacketizer_destroy.restype = None
libopus.opus_repacketizer_destroy.argtypes = [or_p]

def opus_repacketizer_destroy(rp):
    return libopus.opus_repacketizer_destroy(rp)

"""* Add a packet to the current repacketizer state.
  * This packet must match the configuration of any packets already submitted
  * for repacketization since the last call to opus_repacketizer_init().
  * This means that it must have the same coding mode, audio bandwidth, frame
  * size, and channel count.
  * This can be checked in advance by examining the top 6 bits of the first
  * byte of the packet, and ensuring they match the top 6 bits of the first
  * byte of any previously submitted packet.
  * The total duration of audio in the repacketizer state also must not exceed
  * 120 ms, the maximum duration of a single packet, after adding this packet.
  *
  * The contents of the current repacketizer state can be extracted into new
  * packets using opus_repacketizer_out() or opus_repacketizer_out_range().
  *
  * In order to add a packet with a different configuration or to add more
  * audio beyond 120 ms, you must clear the repacketizer state by calling
  * opus_repacketizer_init().
  * If a packet is too large to add to the current repacketizer state, no part
  * of it is added, even if it contains multiple frames, some of which might
  * fit.
  * If you wish to be able to add parts of such packets, you should first use
  * another repacketizer to split the packet into pieces and add them
  * individually.
  * @see opus_repacketizer_out_range
  * @see opus_repacketizer_out
  * @see opus_repacketizer_init
  * @param rp <tt>OpusRepacketizer*</tt>: The repacketizer state to which to
  *                                       add the packet.
  * @param[in] data <tt>const unsigned char*</tt>: The packet data.
  *                                                The application must ensure
  *                                                this pointer remains valid
  *                                                until the next call to
  *                                                opus_repacketizer_init() or
  *                                                opus_repacketizer_destroy().
  * @param len <tt>opus_int32</tt>: The number of bytes in the packet data.
  * @returns An error code indicating whether or not the operation succeeded.
  * @retval #OPUS_OK The packet's contents have been added to the repacketizer
  *                  state.
  * @retval #OPUS_INVALID_PACKET The packet did not have a valid TOC sequence,
  *                              the packet's TOC sequence was not compatible
  *                              with previously submitted packets (because
  *                              the coding mode, audio bandwidth, frame size,
  *                              or channel count did not match), or adding
  *                              this packet would increase the total amount of
  *                              audio stored in the repacketizer state to more
  *                              than 120 ms.
  """
libopus.opus_repacketizer_cat.restype = c_int
libopus.opus_repacketizer_cat.argtypes = [or_p, c_uchar_p, opus_int32]

def opus_repacketizer_cat(rp, data, len):
    return libopus.opus_repacketizer_cat(rp, data, len)


"""* Construct a new packet from data previously submitted to the repacketizer
  * state via opus_repacketizer_cat().
  * @param rp <tt>OpusRepacketizer*</tt>: The repacketizer state from which to
  *                                       construct the new packet.
  * @param begin <tt>int</tt>: The index of the first frame in the current
  *                            repacketizer state to include in the output.
  * @param end <tt>int</tt>: One past the index of the last frame in the
  *                          current repacketizer state to include in the
  *                          output.
  * @param[out] data <tt>const unsigned char*</tt>: The buffer in which to
  *                                                 store the output packet.
  * @param maxlen <tt>opus_int32</tt>: The maximum number of bytes to store in
  *                                    the output buffer. In order to guarantee
  *                                    success, this should be at least
  *                                    <code>1276</code> for a single frame,
  *                                    or for multiple frames,
  *                                    <code>1277*(end-begin)</code>.
  *                                    However, <code>1*(end-begin)</code> plus
  *                                    the size of all packet data submitted to
  *                                    the repacketizer since the last call to
  *                                    opus_repacketizer_init() or
  *                                    opus_repacketizer_create() is also
  *                                    sufficient, and possibly much smaller.
  * @returns The total size of the output packet on success, or an error code
  *          on failure.
  * @retval #OPUS_BAD_ARG <code>[begin,end)</code> was an invalid range of
  *                       frames (begin < 0, begin >= end, or end >
  *                       opus_repacketizer_get_nb_frames()).
  * @retval #OPUS_BUFFER_TOO_SMALL \a maxlen was insufficient to contain the
  *                                complete output packet.
  """
libopus.opus_repacketizer_out_range.restype = opus_int32
libopus.opus_repacketizer_out_range.argtypes = [or_p, c_int, c_int, c_uchar_p, opus_int32]

def opus_repacketizer_out_range(rp, begin, end, data, maxlen):
    return libopus.opus_repacketizer_out_range(rp, begin, end, data, maxlen)

"""* Return the total number of frames contained in packet data submitted to
  * the repacketizer state so far via opus_repacketizer_cat() since the last
  * call to opus_repacketizer_init() or opus_repacketizer_create().
  * This defines the valid range of packets that can be extracted with
  * opus_repacketizer_out_range() or opus_repacketizer_out().
  * @param rp <tt>OpusRepacketizer*</tt>: The repacketizer state containing the
  *                                       frames.
  * @returns The total number of frames contained in the packet data submitted
  *          to the repacketizer state.
  """
libopus.opus_repacketizer_get_nb_frames.restype = c_int
libopus.opus_repacketizer_get_nb_frames.argtypes = [or_p]

def opus_repacketizer_get_nb_frames(rp):
    return libopus.opus_repacketizer_get_nb_frames(rp)

"""* Construct a new packet from data previously submitted to the repacketizer
  * state via opus_repacketizer_cat().
  * This is a convenience routine that returns all the data submitted so far
  * in a single packet.
  * It is equivalent to calling
  * @code
  * opus_repacketizer_out_range(rp, 0, opus_repacketizer_get_nb_frames(rp),
  *                             data, maxlen)
  * @endcode
  * @param rp <tt>OpusRepacketizer*</tt>: The repacketizer state from which to
  *                                       construct the new packet.
  * @param[out] data <tt>const unsigned char*</tt>: The buffer in which to
  *                                                 store the output packet.
  * @param maxlen <tt>opus_int32</tt>: The maximum number of bytes to store in
  *                                    the output buffer. In order to guarantee
  *                                    success, this should be at least
  *                                    <code>1277*opus_repacketizer_get_nb_frames(rp)</code>.
  *                                    However,
  *                                    <code>1*opus_repacketizer_get_nb_frames(rp)</code>
  *                                    plus the size of all packet data
  *                                    submitted to the repacketizer since the
  *                                    last call to opus_repacketizer_init() or
  *                                    opus_repacketizer_create() is also
  *                                    sufficient, and possibly much smaller.
  * @returns The total size of the output packet on success, or an error code
  *          on failure.
  * @retval #OPUS_BUFFER_TOO_SMALL \a maxlen was insufficient to contain the
  *                                complete output packet.
  """
libopus.opus_repacketizer_out.restype = opus_int32
libopus.opus_repacketizer_out.argtypes = [or_p, c_uchar_p, opus_int32]

def opus_repacketizer_out(rp, data, maxlen):
    return libopus.opus_repacketizer_out(rp, data, maxlen)

"""* Pads a given Opus packet to a larger size (possibly changing the TOC sequence).
  * @param[in,out] data <tt>const unsigned char*</tt>: The buffer containing the
  *                                                   packet to pad.
  * @param len <tt>opus_int32</tt>: The size of the packet.
  *                                 This must be at least 1.
  * @param new_len <tt>opus_int32</tt>: The desired size of the packet after padding.
  *                                 This must be at least as large as len.
  * @returns an error code
  * @retval #OPUS_OK \a on success.
  * @retval #OPUS_BAD_ARG \a len was less than 1 or new_len was less than len.
  * @retval #OPUS_INVALID_PACKET \a data did not contain a valid Opus packet.
  """
libopus.opus_packet_pad.restype = c_int
libopus.opus_packet_pad.argtypes = [c_uchar_p, opus_int32, opus_int32]

def opus_packet_pad(data, len, new_len):
    return libopus.opus_packet_pad(data, len, new_len)

"""* Remove all padding from a given Opus packet and rewrite the TOC sequence to
  * minimize space usage.
  * @param[in,out] data <tt>const unsigned char*</tt>: The buffer containing the
  *                                                   packet to strip.
  * @param len <tt>opus_int32</tt>: The size of the packet.
  *                                 This must be at least 1.
  * @returns The new size of the output packet on success, or an error code
  *          on failure.
  * @retval #OPUS_BAD_ARG \a len was less than 1.
  * @retval #OPUS_INVALID_PACKET \a data did not contain a valid Opus packet.
  """
libopus.opus_packet_unpad.restype = opus_int32
libopus.opus_packet_unpad.argtypes = [c_uchar_p, opus_int32]

def opus_packet_unpad(data, len):
    return libopus.opus_packet_unpad(data, len)

"""* Pads a given Opus multi-stream packet to a larger size (possibly changing the TOC sequence).
  * @param[in,out] data <tt>const unsigned char*</tt>: The buffer containing the
  *                                                   packet to pad.
  * @param len <tt>opus_int32</tt>: The size of the packet.
  *                                 This must be at least 1.
  * @param new_len <tt>opus_int32</tt>: The desired size of the packet after padding.
  *                                 This must be at least 1.
  * @param nb_streams <tt>opus_int32</tt>: The number of streams (not channels) in the packet.
  *                                 This must be at least as large as len.
  * @returns an error code
  * @retval #OPUS_OK \a on success.
  * @retval #OPUS_BAD_ARG \a len was less than 1.
  * @retval #OPUS_INVALID_PACKET \a data did not contain a valid Opus packet.
  """
libopus.opus_multistream_packet_pad.restype = c_int
libopus.opus_multistream_packet_pad.argtypes = [c_uchar_p, opus_int32, opus_int32, c_int]

def opus_multistream_packet_pad(data, len, new_len, nb_streams):
    return libopus.opus_multistream_packet_pad(data, len, new_len, nb_streams)

"""* Remove all padding from a given Opus multi-stream packet and rewrite the TOC sequence to
  * minimize space usage.
  * @param[in,out] data <tt>const unsigned char*</tt>: The buffer containing the
  *                                                   packet to strip.
  * @param len <tt>opus_int32</tt>: The size of the packet.
  *                                 This must be at least 1.
  * @param nb_streams <tt>opus_int32</tt>: The number of streams (not channels) in the packet.
  *                                 This must be at least 1.
  * @returns The new size of the output packet on success, or an error code
  *          on failure.
  * @retval #OPUS_BAD_ARG \a len was less than 1 or new_len was less than len.
  * @retval #OPUS_INVALID_PACKET \a data did not contain a valid Opus packet.
  """
libopus.opus_multistream_packet_unpad.restype = opus_int32
libopus.opus_multistream_packet_unpad.argtypes = [c_uchar_p, opus_int32, c_int]

def opus_multistream_packet_unpad(data, len, nb_streams):
    return libopus.opus_multistream_packet_unpad(data, len, nb_streams)
  
# /opus

# opus_multistream

OPUS_MULTISTREAM_GET_ENCODER_STATE_REQUEST =5120
OPUS_MULTISTREAM_GET_DECODER_STATE_REQUEST =5122

class OpusMSEncoder(ctypes.Structure):
    _fields_ = [("dummy", c_int)]
omse_p = POINTER(OpusMSEncoder)

class OpusMSDecoder(ctypes.Structure):
    _fields_ = [("dummy", c_int)]
omsd_p = POINTER(OpusMSDecoder)

libopus.opus_multistream_encoder_get_size.restype = opus_int32
libopus.opus_multistream_encoder_get_size.argtypes = [c_int, c_int]

def opus_multistream_encoder_get_size(streams, coupled_streams):
    return libopus.opus_multistream_encoder_get_size(streams, coupled_streams)

libopus.opus_multistream_surround_encoder_get_size.restype = opus_int32
libopus.opus_multistream_surround_encoder_get_size.argtypes = [c_int, c_int]

def opus_multistream_surround_encoder_get_size(channels, mapping_family):
    return libopus.opus_multistream_surround_encoder_get_size(channels, mapping_family)

libopus.opus_multistream_encoder_create.restype = omse_p
libopus.opus_multistream_encoder_create.argtypes = [opus_int32, c_int, c_int, c_int, c_uchar_p, c_int, c_int_p]

def opus_multistream_encoder_create(Fs, channels,streams,coupled_streams, mapping, application, error):
    return libopus.opus_multistream_encoder_create(Fs, channels,streams,coupled_streams, mapping, application, error)

libopus.opus_multistream_surround_encoder_create.restype = omse_p
libopus.opus_multistream_surround_encoder_create.argtypes = [opus_int32, c_int, c_int, c_int_p, c_int_p, c_uchar_p, c_int, c_int_p]

def opus_multistream_surround_encoder_create(Fs, channels, mapping_family, streams, coupled_streams, mapping, application, error):
    return libopus.opus_multistream_surround_encoder_create(Fs, channels, mapping_family, streams, coupled_streams, mapping, application, error)

libopus.opus_multistream_encoder_init.restype = c_int
libopus.opus_multistream_encoder_init.argtypes = [omse_p, opus_int32, c_int, c_int, c_int, c_uchar_p, c_int]

def opus_multistream_encoder_init(st, Fs, channels, streams, coupled_streams, mapping, application):
    return libopus.opus_multistream_encoder_init(st, Fs, channels, streams, coupled_streams, mapping, application)

libopus.opus_multistream_surround_encoder_init.restype = c_int
libopus.opus_multistream_surround_encoder_init.argtypes = [omse_p, opus_int32, c_int, c_int, c_int_p, c_int_p, c_uchar_p, c_int]

def opus_multistream_surround_encoder_init(st, Fs, channels, mapping_family, streams, coupled_streams, mapping, application):
    return libopus.opus_multistream_surround_encoder_init(st, Fs, channels, mapping_family, streams, coupled_streams, mapping, application)

libopus.opus_multistream_encode.restype = c_int
libopus.opus_multistream_encode.argtypes = [omse_p, opus_int16_p, c_int, c_uchar_p, opus_int32]

def opus_multistream_encode(st, pcm, frame_size, data, max_data_bytes):
    return libopus.opus_multistream_encode(st, pcm, frame_size, data, max_data_bytes)

libopus.opus_multistream_encode_float.restype = c_int
libopus.opus_multistream_encode_float.argtypes = [omse_p, c_float_p, c_int, c_uchar_p, opus_int32]

def opus_multistream_encode_float(st, pcm, frame_size, data, max_data_bytes):
    return libopus.opus_multistream_encode_float(st, pcm, frame_size, data, max_data_bytes)

libopus.opus_multistream_encoder_destroy.restype = None
libopus.opus_multistream_encoder_destroy.argtypes = [omse_p]

def opus_multistream_encoder_destroy(st):
    return libopus.opus_multistream_encoder_destroy(st)

libopus.opus_multistream_encoder_ctl.restype = c_int
libopus.opus_multistream_encoder_ctl.argtypes = [omse_p, c_int]

def opus_multistream_encoder_ctl(st, request):
    return libopus.opus_multistream_encoder_ctl(st, request)

libopus.opus_multistream_decoder_get_size.restype = opus_int32
libopus.opus_multistream_decoder_get_size.argtypes = [c_int, c_int]

def opus_multistream_decoder_get_size(streams, coupled_streams):
    return libopus.opus_multistream_decoder_get_size(streams, coupled_streams)

libopus.opus_multistream_decoder_create.restype = omsd_p
libopus.opus_multistream_decoder_create.argtypes = [opus_int32, c_int, c_int, c_int, c_uchar_p, c_int_p]

def opus_multistream_decoder_create(Fs, channels, streams, coupled_streams, mapping, error):
    return libopus.opus_multistream_decoder_create(Fs, channels, streams, coupled_streams, mapping, error)

libopus.opus_multistream_decoder_init.restype = c_int
libopus.opus_multistream_decoder_init.argtypes = [omsd_p, opus_int32, c_int, c_int, c_int, c_uchar_p]

def opus_multistream_decoder_init(st, Fs, channels, streams, coupled_streams, mapping):
    return libopus.opus_multistream_decoder_init(st, Fs, channels, streams, coupled_streams, mapping)

libopus.opus_multistream_decode.restype = c_int
libopus.opus_multistream_decode.argtypes = [omsd_p, c_uchar_p, opus_int32, opus_int16_p, c_int, c_int]

def opus_multistream_decode(st, data, len, pcm, frame_size, decode_fec):
    return libopus.opus_multistream_decode(st, data, len, pcm, frame_size, decode_fec)

libopus.opus_multistream_decode_float.restype = c_int
libopus.opus_multistream_decode_float.argtypes = [omsd_p, c_uchar_p, opus_int32, c_float_p, c_int, c_int]

def opus_multistream_decode_float(st, data, len, pcm, frame_size, decode_fec):
    return libopus.opus_multistream_decode_float(st, data, len, pcm, frame_size, decode_fec)

libopus.opus_multistream_decoder_ctl.restype = c_int
libopus.opus_multistream_decoder_ctl.argtypes = [omsd_p, c_int]

def opus_multistream_decoder_ctl(st, request):
    return libopus.opus_multistream_decoder_ctl(st, request)

libopus.opus_multistream_decoder_destroy.restype = None
libopus.opus_multistream_decoder_destroy.argtypes = [omsd_p]

def opus_multistream_decoder_destroy(st):
    return libopus.opus_multistream_decoder_destroy(st)

# /opus_multistream

# opusfile

class OggOpusFile(ctypes.Structure):
    _fields_ = [("dummy", c_int)]

oof_p = POINTER(OggOpusFile)

OP_FALSE         =(-1)
OP_EOF           =(-2)
OP_HOLE          =(-3)
OP_EREAD         =(-128)
OP_EFAULT        =(-129)
OP_EIMPL         =(-130)
OP_EINVAL        =(-131)
OP_ENOTFORMAT    =(-132)
OP_EBADHEADER    =(-133)
OP_EVERSION      =(-134)
OP_ENOTAUDIO     =(-135)
OP_EBADPACKET    =(-136)
OP_EBADLINK      =(-137)
OP_ENOSEEK       =(-138)
OP_EBADTIMESTAMP =(-139)


OPUS_CHANNEL_COUNT_MAX =(255)

class OpusHead(ctypes.Structure):
    _fields_ = [("version", c_int),
                ("channel_count", c_int),
                ("pre_skip", c_uint),
                ("input_sample_rate", opus_uint32),
                ("output_gain", c_int),
                ("mapping_family", c_int),
                ("stream_count", c_int),
                ("coupled_count", c_int),
                ("mapping", c_uchar * OPUS_CHANNEL_COUNT_MAX)]

oh_p = POINTER(OpusHead)

class OpusTags(ctypes.Structure):
    _fields_ = [("user_comments", c_char_p_p),
                ("comment_lengths", c_int_p),
                ("comments", c_int),
                ("vendor", c_char_p)]

ot_p = POINTER(OpusTags)

OP_PIC_FORMAT_UNKNOWN =(-1)
OP_PIC_FORMAT_URL     =(0)
OP_PIC_FORMAT_JPEG    =(1)
OP_PIC_FORMAT_PNG     =(2)
OP_PIC_FORMAT_GIF     =(3)

class OpusPictureTag(ctypes.Structure):
    _fields_ = [("type", opus_int32),
                ("mime_type", c_char_p),
                ("description", c_char_p),
                ("width", opus_uint32),
                ("height", opus_uint32),
                ("depth", opus_uint32),
                ("colors", opus_uint32),
                ("data_length", opus_uint32),
                ("data", c_uchar_p),
                ("format", c_int)]

opt_p = POINTER(OpusPictureTag)

libopusfile.opus_head_parse.restype = c_int
libopusfile.opus_head_parse.argtypes = [oh_p, c_uchar_p, c_size_t]

def opus_head_parse(_head, _data, _len):
    return libopusfile.opus_head_parse(_head, _data, _len)

libopusfile.opus_granule_sample.restype = ogg_int64_t
libopusfile.opus_granule_sample.argtypes = [oh_p, ogg_int64_t]

def opus_granule_sample(_head, _gp):
    return libopusfile.opus_granule_sample(_head, _gp)

libopusfile.opus_tags_parse.restype = c_int
libopusfile.opus_tags_parse.argtypes = [ot_p, c_uchar_p, c_size_t]

def opus_tags_parse(_tags, _data, _len):
    return libopusfile.opus_tags_parse(_tags, _data, _len)

libopusfile.opus_tags_copy.restype = c_int
libopusfile.opus_tags_copy.argtypes = [ot_p, ot_p]

def opus_tags_copy(_dst, _src):
    return libopusfile.opus_tags_copy(_dst, _src)

libopusfile.opus_tags_init.restype = None
libopusfile.opus_tags_init.argtypes = [ot_p]

def opus_tags_init(_tags):
    return libopusfile.opus_tags_init(_tags)

libopusfile.opus_tags_add.restype = c_int
libopusfile.opus_tags_add.argtypes = [ot_p, c_char_p, c_char_p]

def opus_tags_add(_tags, _tag, _value):
    return libopusfile.opus_tags_add(_tags, _tag, _value)

libopusfile.opus_tags_add_comment.restype = c_int
libopusfile.opus_tags_add_comment.argtypes = [ot_p, c_char_p]

def opus_tags_add_comment(_tags, _comment):
    return libopusfile.opus_tags_add_comment(_tags, _comment)

libopusfile.opus_tags_set_binary_suffix.restype = c_int
libopusfile.opus_tags_set_binary_suffix.argtypes = [ot_p, c_uchar_p, c_int]

def opus_tags_set_binary_suffix(_tags, _data, _len):
    return libopusfile.opus_tags_set_binary_suffix(_tags, _data, _len)

libopusfile.opus_tags_query.restype = c_char_p
libopusfile.opus_tags_query.argtypes = [ot_p, c_char_p, c_int]

def opus_tags_query(_tags, _tag, _count):
    return libopusfile.opus_tags_query(_tags, _tag, _count)

libopusfile.opus_tags_query_count.restype = c_int
libopusfile.opus_tags_query_count.argtypes = [ot_p, c_char_p]

def opus_tags_query_count(_tags, _tag):
    return libopusfile.opus_tags_query_count(_tags, _tag)

libopusfile.opus_tags_get_binary_suffix.restype = c_uchar_p
libopusfile.opus_tags_get_binary_suffix.argtypes = [ot_p, c_int_p]

def opus_tags_get_binary_suffix(_tags, _len):
    return libopusfile.opus_tags_get_binary_suffix(_tags, _len)

libopusfile.opus_tags_get_album_gain.restype = c_int
libopusfile.opus_tags_get_album_gain.argtypes = [ot_p, c_int_p]

def opus_tags_get_album_gain(_tags, _gain_q8):
    return libopusfile.opus_tags_get_album_gain(_tags, _gain_q8)

libopusfile.opus_tags_get_track_gain.restype = c_int
libopusfile.opus_tags_get_track_gain.argtypes = [ot_p, c_int_p]

def opus_tags_get_track_gain(_tags, _gain_q8):
    return libopusfile.opus_tags_get_track_gain(_tags, _gain_q8)

libopusfile.opus_tags_clear.restype = None
libopusfile.opus_tags_clear.argtypes = [ot_p]

def opus_tags_clear(_tags):
    return libopusfile.opus_tags_clear(_tags)

libopusfile.opus_tagcompare.restype = c_int
libopusfile.opus_tagcompare.argtypes = [c_char_p, c_char_p]

def opus_tagcompare(_tag_name, _comment):
    return libopusfile.opus_tagcompare(_tag_name, _comment)

libopusfile.opus_tagncompare.restype = c_int
libopusfile.opus_tagncompare.argtypes = [c_char_p, c_int, c_char_p]

def opus_tagncompare(_tag_name, _tag_len, _comment):
    return libopusfile.opus_tagncompare(_tag_name, _tag_len, _comment)

libopusfile.opus_picture_tag_parse.restype = c_int
libopusfile.opus_picture_tag_parse.argtypes = [opt_p, c_char_p]

def opus_picture_tag_parse(_pic, _tag):
    return libopusfile.opus_picture_tag_parse(_pic, _tag)

libopusfile.opus_picture_tag_init.restype = None
libopusfile.opus_picture_tag_init.argtypes = [opt_p]

def opus_picture_tag_init(_pic):
    return libopusfile.opus_picture_tag_init(_pic)

libopusfile.opus_picture_tag_clear.restype = None
libopusfile.opus_picture_tag_clear.argtypes = [opt_p]

def opus_picture_tag_clear(_pic):
    return libopusfile.opus_picture_tag_clear(_pic)

OP_SSL_SKIP_CERTIFICATE_CHECK_REQUEST =(6464)
OP_HTTP_PROXY_HOST_REQUEST            =(6528)
OP_HTTP_PROXY_PORT_REQUEST            =(6592)
OP_HTTP_PROXY_USER_REQUEST            =(6656)
OP_HTTP_PROXY_PASS_REQUEST            =(6720)
OP_GET_SERVER_INFO_REQUEST            =(6784)

class OpusServerInfo(ctypes.Structure):
    _fields_ = [("name", c_char_p),
                ("description", c_char_p),
                ("genre", c_char_p),
                ("url", c_char_p),
                ("server", c_char_p),
                ("content_type", c_char_p),
                ("bitrate_kbps", opus_int32),
                ("is_public", c_int),
                ("is_ssl", c_int)]

osi_p = POINTER(OpusServerInfo)
try:
    libopusfile.opus_server_info_init.restype = None
    libopusfile.opus_server_info_init.argtypes = [osi_p]

    def opus_server_info_init(_info):
        return libopusfile.opus_server_info_init(_info)

    libopusfile.opus_server_info_clear.restype = None
    libopusfile.opus_server_info_clear.argtypes = [osi_p]

    def opus_server_info_clear(_info):
        return libopusfile.opus_server_info_clear(_info)
except:
    pass

op_read_func = ctypes.CFUNCTYPE(c_int,
                                c_void_p,
                                c_uchar_p,
                                c_int)

op_seek_func = ctypes.CFUNCTYPE(c_int,
                                c_void_p,
                                opus_int64,
                                c_int)

op_tell_func = ctypes.CFUNCTYPE(opus_int64,
                                c_void_p)

op_close_func = ctypes.CFUNCTYPE(c_int,
                                c_void_p)

class OpusFileCallbacks(ctypes.Structure):
    _fields_ = [("read", op_read_func),
                ("seek", op_seek_func),
                ("tell", op_tell_func),
                ("close", op_close_func)]

ofc_p = POINTER(OpusFileCallbacks)

libopusfile.op_fopen.restype = c_void_p
libopusfile.op_fopen.argtypes = [ofc_p, c_char_p, c_char_p]

def op_fopen(_cb, _path, _mode):
    return libopusfile.op_fopen(_cb, _path, _mode)

libopusfile.op_fdopen.restype = c_void_p
libopusfile.op_fdopen.argtypes = [ofc_p, c_int, c_char_p]

def op_fdopen(_cb, _fd, _mode):
    return libopusfile.op_fdopen(_cb, _fd, _mode)

libopusfile.op_freopen.restype = c_void_p
libopusfile.op_freopen.argtypes = [ofc_p, c_char_p, c_char_p, c_void_p]

def op_freopen(_cb, _path, _mode, _stream):
    return libopusfile.op_freopen(_cb, _path, _mode, _stream)

libopusfile.op_mem_stream_create.restype = c_void_p
libopusfile.op_mem_stream_create.argtypes = [ofc_p, c_uchar_p, c_size_t]

def op_mem_stream_create(_cb, _data, _size):
    return libopusfile.op_mem_stream_create(_cb, _data, _size)

##libopusfile.op_url_stream_vcreate.restype = c_void_p
##libopusfile.op_url_stream_vcreate.argtypes = [ofc_p, c_char_p, ]
##
##def op_url_stream_vcreate(hhhh):
##    return libopusfile.op_url_stream_vcreate(hhhhhhh)
##
##OP_WARN_UNUSED_RESULT void *op_url_stream_vcreate(OpusFileCallbacks *_cb,
## const char *_url,va_list _ap) OP_ARG_NONNULL(1) OP_ARG_NONNULL(2);

##libopusfile.oooooo.restype = hhhh
##libopusfile.ooooooo.argtypes = [hhh]
##
##def ooooo(hhhh):
##    return libopusfile.ooooo(hhhhhhh)
##
##OP_WARN_UNUSED_RESULT void *op_url_stream_create(OpusFileCallbacks *_cb,
## const char *_url,...) OP_ARG_NONNULL(1) OP_ARG_NONNULL(2);

libopusfile.op_test.restype = c_int
libopusfile.op_test.argtypes = [oh_p, c_uchar_p, c_size_t]

def op_test(_head, _initial_data, _initial_bytes):
    return libopusfile.op_test(_head, _initial_data, _initial_bytes)

libopusfile.op_open_file.restype = oof_p
libopusfile.op_open_file.argtypes = [c_char_p, c_int_p]

def op_open_file(_path, _error):
    return libopusfile.op_open_file(_path, _error)

libopusfile.op_open_memory.restype = oof_p
libopusfile.op_open_memory.argtypes = [c_uchar_p, c_size_t, c_int_p]

def op_open_memory(_data, _size, _error):
    return libopusfile.op_open_memory(_data, _size, _error)

##libopusfile.oooooo.restype = hhhh
##libopusfile.ooooooo.argtypes = [hhh]
##
##def ooooo(hhhh):
##    return libopusfile.ooooo(hhhhhhh)
##
##OP_WARN_UNUSED_RESULT OggOpusFile *op_vopen_url(const char *_url,
## int *_error,va_list _ap) OP_ARG_NONNULL(1);

##libopusfile.oooooo.restype = hhhh
##libopusfile.ooooooo.argtypes = [hhh]
##
##def ooooo(hhhh):
##    return libopusfile.ooooo(hhhhhhh)
##
##OP_WARN_UNUSED_RESULT OggOpusFile *op_open_url(const char *_url,
## int *_error,...) OP_ARG_NONNULL(1);

libopusfile.op_open_callbacks.restype = oof_p
libopusfile.op_open_callbacks.argtypes = [c_void_p, ofc_p, c_uchar_p, c_size_t, c_int_p]

def op_open_callbacks(_source, _cb, _initial_data, _initial_bytes, _error):
    return libopusfile.op_open_callbacks(_source, _cb, _initial_data, _initial_bytes, _error)

libopusfile.op_test_file.restype = oof_p
libopusfile.op_test_file.argtypes = [c_char_p, c_int_p]

def op_test_file(_path, _error):
    return libopusfile.op_test_file(_path, _error)

libopusfile.op_test_memory.restype = oof_p
libopusfile.op_test_memory.argtypes = [c_uchar_p, c_size_t, c_int_p]

def op_test_memory(_data, _size, _error):
    return libopusfile.op_test_memory(_data, _size, _error)

##libopusfile.oooooo.restype = hhhh
##libopusfile.ooooooo.argtypes = [hhh]
##
##def ooooo(hhhh):
##    return libopusfile.ooooo(hhhhhhh)
##
##OP_WARN_UNUSED_RESULT OggOpusFile *op_vtest_url(const char *_url,
## int *_error,va_list _ap) OP_ARG_NONNULL(1);

##libopusfile.oooooo.restype = hhhh
##libopusfile.ooooooo.argtypes = [hhh]
##
##def ooooo(hhhh):
##    return libopusfile.ooooo(hhhhhhh)
##
##OP_WARN_UNUSED_RESULT OggOpusFile *op_test_url(const char *_url,
## int *_error,...) OP_ARG_NONNULL(1);

libopusfile.op_test_callbacks.restype = oof_p
libopusfile.op_test_callbacks.argtypes = [c_void_p, ofc_p, c_uchar_p, c_size_t, c_int_p]

def op_test_callbacks(_source, _cb, _initial_data, _initial_bytes, _error):
    return libopusfile.op_test_callbacks(_source, _cb, _initial_data, _initial_bytes, _error)

libopusfile.op_test_open.restype = c_int
libopusfile.op_test_open.argtypes = [oof_p]

def op_test_open(_of):
    return libopusfile.op_test_open(_of)

libopusfile.op_free.restype = None
libopusfile.op_free.argtypes = [oof_p]

def op_free(_of):
    return libopusfile.op_free(_of)

libopusfile.op_seekable.restype = c_int
libopusfile.op_seekable.argtypes = [oof_p]

def op_seekable(_of):
    return libopusfile.op_seekable(_of)

libopusfile.op_link_count.restype = c_int
libopusfile.op_link_count.argtypes = [oof_p]

def op_link_count(_of):
    return libopusfile.op_link_count(_of)

libopusfile.op_serialno.restype = opus_uint32
libopusfile.op_serialno.argtypes = [oof_p, c_int]

def op_serialno(_of, _li):
    return libopusfile.op_serialno(_of, _li)

libopusfile.op_channel_count.restype = c_int
libopusfile.op_channel_count.argtypes = [oof_p, c_int]

def op_channel_count(_of, _li):
    return libopusfile.op_channel_count(_of, _li)

libopusfile.op_raw_total.restype = opus_int64
libopusfile.op_raw_total.argtypes = [oof_p, c_int]

def op_raw_total(_of, _li):
    return libopusfile.op_raw_total(_of, _li)

libopusfile.op_pcm_total.restype = ogg_int64_t
libopusfile.op_pcm_total.argtypes = [oof_p, c_int]

def op_pcm_total(_of, _li):
    return libopusfile.op_pcm_total(_of, _li)

libopusfile.op_head.restype = oh_p
libopusfile.op_head.argtypes = [oof_p, c_int]

def op_head(_of, _li):
    return libopusfile.op_head(_of, _li)

libopusfile.op_tags.restype = ot_p
libopusfile.op_tags.argtypes = [oof_p, c_int]

def op_tags(_of, _li):
    return libopusfile.op_tags(_of, _li)

libopusfile.op_current_link.restype = c_int
libopusfile.op_current_link.argtypes = [oof_p]

def op_current_link(_of):
    return libopusfile.op_current_link(_of)

libopusfile.op_bitrate.restype = opus_int32
libopusfile.op_bitrate.argtypes = [oof_p, c_int]

def op_bitrate(_of, _li):
    return libopusfile.op_bitrate(_of, _li)

libopusfile.op_bitrate_instant.restype = opus_int32
libopusfile.op_bitrate_instant.argtypes = [oof_p]

def op_bitrate_instant(_of):
    return libopusfile.op_bitrate_instant(_of)

libopusfile.op_raw_tell.restype = opus_int64
libopusfile.op_raw_tell.argtypes = [oof_p]

def op_raw_tell(_of):
    return libopusfile.op_raw_tell(_of)

libopusfile.op_pcm_tell.restype = ogg_int64_t
libopusfile.op_pcm_tell.argtypes = [oof_p]

def op_pcm_tell(_of):
    return libopusfile.op_pcm_tell(_of)

libopusfile.op_raw_seek.restype = c_int
libopusfile.op_raw_seek.argtypes = [oof_p, opus_int64]

def op_raw_seek(_of, _byte_offset):
    return libopusfile.op_raw_seek(_of, _byte_offset)

libopusfile.op_pcm_seek.restype = c_int
libopusfile.op_pcm_seek.argtypes = [oof_p,ogg_int64_t]

def op_pcm_seek(_of, _pcm_offset):
    return libopusfile.op_pcm_seek(_of, _pcm_offset)

OP_DEC_FORMAT_SHORT =(7008)
OP_DEC_FORMAT_FLOAT =(7040)
OP_DEC_USE_DEFAULT  =(6720)

op_decode_cb_func = ctypes.CFUNCTYPE(c_int,
                                     c_void_p,
                                     omsd_p,
                                     c_void_p,
                                     op_p,
                                     c_int,
                                     c_int,
                                     c_int,
                                     c_int)

libopusfile.op_set_decode_callback.restype = None
libopusfile.op_set_decode_callback.argtypes = [oof_p, op_decode_cb_func, c_void_p]

def op_set_decode_callback(_of, _decode_cb, _ctx):
    return libopusfile.op_set_decode_callback(_of, _decode_cb, _ctx)

OP_HEADER_GAIN   =(0)
OP_ALBUM_GAIN    =(3007)
OP_TRACK_GAIN    =(3008)
OP_ABSOLUTE_GAIN =(3009)

libopusfile.op_set_gain_offset.restype = c_int
libopusfile.op_set_gain_offset.argtypes = [oof_p, c_int, opus_int32]

def op_set_gain_offset(_of, _gain_type, _gain_offset_q8):
    return libopusfile.op_set_gain_offset(_of, _gain_type, _gain_offset_q8)

libopusfile.op_set_dither_enabled.restype = None
libopusfile.op_set_dither_enabled.argtypes = [oof_p, c_int]

def op_set_dither_enabled(_of, _enabled):
    return libopusfile.op_set_dither_enabled(_of, _enabled)

libopusfile.op_read.restype = c_int
libopusfile.op_read.argtypes = [oof_p, opus_int16_p, c_int, c_int_p]

def op_read(_of, _pcm, _buf_size, _li):
    return libopusfile.op_read(_of, _pcm, _buf_size, _li)

libopusfile.op_read_float.restype = c_int
libopusfile.op_read_float.argtypes = [oof_p, c_float_p, c_int, c_int_p]

def op_read_float(_of, _pcm, _buf_size, _li):
    return libopusfile.op_read_float(_of, _pcm, _buf_size, _li)

libopusfile.op_read_stereo.restype = c_int
libopusfile.op_read_stereo.argtypes = [oof_p, opus_int16_p, c_int]

def op_read_stereo(_of, _pcm, _buf_size):
    return libopusfile.op_read_stereo(_of, _pcm, _buf_size)

libopusfile.op_read_float_stereo.restype = c_int
libopusfile.op_read_float_stereo.argtypes = [oof_p, c_float_p, c_int]

def op_read_float_stereo(_of, _pcm, _buf_size):
    return libopusfile.op_read_float_stereo(_of, _pcm, _buf_size)
