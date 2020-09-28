% Intrinsic and Extrinsic Camera Parameters
%
% This script file can be directly executed under Matlab to recover the camera intrinsic and extrinsic parameters.
% IMPORTANT: This file contains neither the structure of the calibration objects nor the image coordinates of the calibration points.
%            All those complementary variables are saved in the complete matlab data file Calib_Results.mat.
% For more information regarding the calibration model visit http://www.vision.caltech.edu/bouguetj/calib_doc/


%-- Focal length:
fc = [ 1295.664946456044618 ; 1280.534520146036584 ];

%-- Principal point:
cc = [ 915.601244442951838 ; 478.745455831792412 ];

%-- Skew coefficient:
alpha_c = 0.000000000000000;

%-- Distortion coefficients:
kc = [ 0.066455132342023 ; 0.279518966478502 ; -0.002214579341478 ; -0.008018103160971 ; 0.000000000000000 ];

%-- Focal length uncertainty:
fc_error = [ 53.927647449705255 ; 48.745178919406676 ];

%-- Principal point uncertainty:
cc_error = [ 21.559657966286998 ; 39.714558819914949 ];

%-- Skew coefficient uncertainty:
alpha_c_error = 0.000000000000000;

%-- Distortion coefficients uncertainty:
kc_error = [ 0.083592634829084 ; 0.846191174503302 ; 0.008947151788718 ; 0.007447418725482 ; 0.000000000000000 ];

%-- Image size:
nx = 1920;
ny = 1080;


%-- Various other variables (may be ignored if you do not use the Matlab Calibration Toolbox):
%-- Those variables are used to control which intrinsic parameters should be optimized

n_ima = 24;						% Number of calibration images
est_fc = [ 1 ; 1 ];					% Estimation indicator of the two focal variables
est_aspect_ratio = 1;				% Estimation indicator of the aspect ratio fc(2)/fc(1)
center_optim = 1;					% Estimation indicator of the principal point
est_alpha = 0;						% Estimation indicator of the skew coefficient
est_dist = [ 1 ; 1 ; 1 ; 1 ; 0 ];	% Estimation indicator of the distortion coefficients


%-- Extrinsic parameters:
%-- The rotation (omc_kk) and the translation (Tc_kk) vectors for every calibration image and their uncertainties

%-- Image #1:
omc_1 = [ 2.31357 ; 1.78459 ; -0.554941 ];
Tc_1  = [ -0.180863 ; -0.0818014 ; 1.01929 ];
omc_error_1 = [ 0.015749 ; 0.0191459 ; 0.0353811 ];
Tc_error_1  = [ 0.0170589 ; 0.0313954 ; 0.0414388 ];

%-- Image #2:
omc_2 = [ NaN ; NaN ; NaN ];
Tc_2  = [ NaN ; NaN ; NaN ];
omc_error_2 = [ NaN ; NaN ; NaN ];
Tc_error_2  = [ NaN ; NaN ; NaN ];

%-- Image #3:
omc_3 = [ NaN ; NaN ; NaN ];
Tc_3  = [ NaN ; NaN ; NaN ];
omc_error_3 = [ NaN ; NaN ; NaN ];
Tc_error_3  = [ NaN ; NaN ; NaN ];

%-- Image #4:
omc_4 = [ 2.34325 ; 1.78527 ; -0.555491 ];
Tc_4  = [ -0.176799 ; -0.0656441 ; 0.883818 ];
omc_error_4 = [ 0.0150199 ; 0.0188401 ; 0.0354381 ];
Tc_error_4  = [ 0.0148064 ; 0.0272594 ; 0.0358074 ];

%-- Image #5:
omc_5 = [ NaN ; NaN ; NaN ];
Tc_5  = [ NaN ; NaN ; NaN ];
omc_error_5 = [ NaN ; NaN ; NaN ];
Tc_error_5  = [ NaN ; NaN ; NaN ];

%-- Image #6:
omc_6 = [ NaN ; NaN ; NaN ];
Tc_6  = [ NaN ; NaN ; NaN ];
omc_error_6 = [ NaN ; NaN ; NaN ];
Tc_error_6  = [ NaN ; NaN ; NaN ];

%-- Image #7:
omc_7 = [ NaN ; NaN ; NaN ];
Tc_7  = [ NaN ; NaN ; NaN ];
omc_error_7 = [ NaN ; NaN ; NaN ];
Tc_error_7  = [ NaN ; NaN ; NaN ];

%-- Image #8:
omc_8 = [ NaN ; NaN ; NaN ];
Tc_8  = [ NaN ; NaN ; NaN ];
omc_error_8 = [ NaN ; NaN ; NaN ];
Tc_error_8  = [ NaN ; NaN ; NaN ];

%-- Image #9:
omc_9 = [ 2.05221 ; 2.24569 ; -0.379752 ];
Tc_9  = [ -0.0573809 ; -0.132134 ; 0.574948 ];
omc_error_9 = [ 0.0117779 ; 0.0170305 ; 0.030264 ];
Tc_error_9  = [ 0.00962024 ; 0.0173793 ; 0.0236852 ];

%-- Image #10:
omc_10 = [ NaN ; NaN ; NaN ];
Tc_10  = [ NaN ; NaN ; NaN ];
omc_error_10 = [ NaN ; NaN ; NaN ];
Tc_error_10  = [ NaN ; NaN ; NaN ];

%-- Image #11:
omc_11 = [ NaN ; NaN ; NaN ];
Tc_11  = [ NaN ; NaN ; NaN ];
omc_error_11 = [ NaN ; NaN ; NaN ];
Tc_error_11  = [ NaN ; NaN ; NaN ];

%-- Image #12:
omc_12 = [ NaN ; NaN ; NaN ];
Tc_12  = [ NaN ; NaN ; NaN ];
omc_error_12 = [ NaN ; NaN ; NaN ];
Tc_error_12  = [ NaN ; NaN ; NaN ];

%-- Image #13:
omc_13 = [ 1.09001 ; 2.70075 ; -0.16235 ];
Tc_13  = [ 0.0125093 ; -0.137421 ; 0.529472 ];
omc_error_13 = [ 0.0105735 ; 0.0195406 ; 0.0283592 ];
Tc_error_13  = [ 0.00885381 ; 0.0161217 ; 0.0214904 ];

%-- Image #14:
omc_14 = [ NaN ; NaN ; NaN ];
Tc_14  = [ NaN ; NaN ; NaN ];
omc_error_14 = [ NaN ; NaN ; NaN ];
Tc_error_14  = [ NaN ; NaN ; NaN ];

%-- Image #15:
omc_15 = [ NaN ; NaN ; NaN ];
Tc_15  = [ NaN ; NaN ; NaN ];
omc_error_15 = [ NaN ; NaN ; NaN ];
Tc_error_15  = [ NaN ; NaN ; NaN ];

%-- Image #16:
omc_16 = [ NaN ; NaN ; NaN ];
Tc_16  = [ NaN ; NaN ; NaN ];
omc_error_16 = [ NaN ; NaN ; NaN ];
Tc_error_16  = [ NaN ; NaN ; NaN ];

%-- Image #17:
omc_17 = [ 1.48216 ; 2.49416 ; -0.397643 ];
Tc_17  = [ 0.0498856 ; -0.107759 ; 0.594841 ];
omc_error_17 = [ 0.0122109 ; 0.0183503 ; 0.0278769 ];
Tc_error_17  = [ 0.00986784 ; 0.0181021 ; 0.0241744 ];

%-- Image #18:
omc_18 = [ NaN ; NaN ; NaN ];
Tc_18  = [ NaN ; NaN ; NaN ];
omc_error_18 = [ NaN ; NaN ; NaN ];
Tc_error_18  = [ NaN ; NaN ; NaN ];

%-- Image #19:
omc_19 = [ NaN ; NaN ; NaN ];
Tc_19  = [ NaN ; NaN ; NaN ];
omc_error_19 = [ NaN ; NaN ; NaN ];
Tc_error_19  = [ NaN ; NaN ; NaN ];

%-- Image #20:
omc_20 = [ NaN ; NaN ; NaN ];
Tc_20  = [ NaN ; NaN ; NaN ];
omc_error_20 = [ NaN ; NaN ; NaN ];
Tc_error_20  = [ NaN ; NaN ; NaN ];

%-- Image #21:
omc_21 = [ 1.85743 ; 2.17356 ; -0.601966 ];
Tc_21  = [ -0.129276 ; -0.102142 ; 0.731808 ];
omc_error_21 = [ 0.0116243 ; 0.0200244 ; 0.0339964 ];
Tc_error_21  = [ 0.0122365 ; 0.0224085 ; 0.029565 ];

%-- Image #22:
omc_22 = [ NaN ; NaN ; NaN ];
Tc_22  = [ NaN ; NaN ; NaN ];
omc_error_22 = [ NaN ; NaN ; NaN ];
Tc_error_22  = [ NaN ; NaN ; NaN ];

%-- Image #23:
omc_23 = [ NaN ; NaN ; NaN ];
Tc_23  = [ NaN ; NaN ; NaN ];
omc_error_23 = [ NaN ; NaN ; NaN ];
Tc_error_23  = [ NaN ; NaN ; NaN ];

%-- Image #24:
omc_24 = [ -2.04212 ; -2.05582 ; 1.05925 ];
Tc_24  = [ -0.0775983 ; -0.142626 ; 0.689044 ];
omc_error_24 = [ 0.0193578 ; 0.01379 ; 0.0424525 ];
Tc_error_24  = [ 0.0116971 ; 0.0211394 ; 0.0261019 ];

