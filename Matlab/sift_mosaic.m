function mosaic = sift_mosaic(im1, im2, display)
% SIFT_MOSAIC Demonstrates matching two images using SIFT and RANSAC
%
%   SIFT_MOSAIC demonstrates matching two images based on SIFT
%   features and RANSAC and computing their mosaic.
%
%   SIFT_MOSAIC by itself runs the algorithm on two standard test
%   images. Use SIFT_MOSAIC(IM1,IM2) to compute the mosaic of two
%   custom images IM1 and IM2.

% AUTORIGHTS


% if nargin == 0
%   im1 = imread(fullfile(vl_root, 'data', 'river1.jpg')) ;
%   im2 = imread(fullfile(vl_root, 'data', 'river2.jpg')) ;
% else
%   im1 = imread(im1) ;
%   im2 = imread(im2) ;
% end

% make single
im1 = im2single(im1) ;
im2 = im2single(im2) ; 

% make grayscale
if size(im1,3) > 1, im1g = rgb2gray(im1) ; else im1g = im1 ; end
if size(im2,3) > 1, im2g = rgb2gray(im2) ; else im2g = im2 ; end


% --------------------------------------------------------------------
%                                                         SIFT matches
% --------------------------------------------------------------------
% f(x,y,radius,orientation)
% 
[f1,d1] = vl_sift(im1g) ;
[f2,d2] = vl_sift(im2g) ;

% scores are the squared euclidean distance between matches
[matches, scores] = vl_ubcmatch(d1,d2) ;

numMatches = size(matches,2) ;

% X1 is the match coord. of image 1's SIFT feats
% X2 is the match coord. of image 2's SIFT feats
% w/ 3rd column = 1
X1 = f1(1:2,matches(1,:)) ; X1(3,:) = 1 ;
X2 = f2(1:2,matches(2,:)) ; X2(3,:) = 1 ;

% --------------------------------------------------------------------
%                                         RANSAC with homography model
% --------------------------------------------------------------------

clear H score ok ;
for t = 1:100
  % estimate homograpyh:
  % random subset of 4 columns of the number of matches
  subset = vl_colsubset(1:numMatches, 4) ;
  A = [] ;
  for i = subset
    % Concatenate the Kronecker tensor product of X1 and X2hat to matrix A
    % of the random subset (kron is all the possible products between
    % elements of X1 and X2hat)
    A = cat(1, A, kron(X1(:,i)', vl_hat(X2(:,i)))) ;
  end
  
  % produce a diagonal matrix S of the same dimension as A, with
  % nonnegative diagonal elements in decreasing order, and unitary matrices 
  % U and V so that A = U*S*V'.
  [U,S,V] = svd(A) ;
  
  % reshape the 9th element in V to a 3x3 matrix and add to the t-th
  % element of H
  H{t} = reshape(V(:,9),3,3) ;

  % score homography:
  % X2_ is an approx. du is the difference between the approx x value and
  % the real x val
  % dv is the difference between the approx y value and the real y value
  X2_ = H{t} * X1 ;
  du = X2_(1,:)./X2_(3,:) - X2(1,:)./X2(3,:) ;
  dv = X2_(2,:)./X2_(3,:) - X2(2,:)./X2(3,:) ;
  % ok{t} is 1 if the squared euclidean diff is less than 6*6, the score is
  % the sum of ok
  ok{t} = (du.*du + dv.*dv) < 6*6 ;
  score(t) = sum(ok{t}) ;
end

% Find the best homography and the best ok
[score, best] = max(score) ;
H = H{best} ;
ok = ok{best} ;

% --------------------------------------------------------------------
%                                                  Optional refinement
% --------------------------------------------------------------------

function err = residual(H)
 u = H(1) * X1(1,ok) + H(4) * X1(2,ok) + H(7) ;
 v = H(2) * X1(1,ok) + H(5) * X1(2,ok) + H(8) ;
 d = H(3) * X1(1,ok) + H(6) * X1(2,ok) + 1 ;
 du = X2(1,ok) - u ./ d ;
 dv = X2(2,ok) - v ./ d ;
 err = sum(du.*du + dv.*dv) ;
end

if exist('fminsearch') == 2
  H = H / H(3,3) ;
  opts = optimset('Display', 'none', 'TolFun', 1e-8, 'TolX', 1e-8) ;
  H(1:8) = fminsearch(@residual, H(1:8)', opts) ;
else
  warning('Refinement disabled as fminsearch was not found.') ;
end

% --------------------------------------------------------------------
%                                                         Show matches
% --------------------------------------------------------------------
if display == 1
    dh1 = max(size(im2,1)-size(im1,1),0) ;
    dh2 = max(size(im1,1)-size(im2,1),0) ;
    
    % show the tentative matches
    figure(1) ; clf ;
    subplot(2,1,1) ;
    imagesc([padarray(im1,dh1,'post') padarray(im2,dh2,'post')]) ;
    o = size(im1,2) ;
    line([f1(1,matches(1,:));f2(1,matches(2,:))+o], ...
         [f1(2,matches(1,:));f2(2,matches(2,:))]) ;
    title(sprintf('%d tentative matches', numMatches)) ;
    axis image off ;
    
    % show the best matches from the RANSAC homography
    subplot(2,1,2) ;
    imagesc([padarray(im1,dh1,'post') padarray(im2,dh2,'post')]) ;
    o = size(im1,2) ;
    line([f1(1,matches(1,ok));f2(1,matches(2,ok))+o], ...
         [f1(2,matches(1,ok));f2(2,matches(2,ok))]) ;
    title(sprintf('%d (%.2f%%) inliner matches out of %d', ...
                  sum(ok), ...
                  100*sum(ok)/numMatches, ...
                  numMatches)) ;
    axis image off ;

    drawnow ;
end

% --------------------------------------------------------------------
%                                                               Mosaic
% --------------------------------------------------------------------


box2 = [1  size(im2,2) size(im2,2)  1 ;
        1  1           size(im2,1)  size(im2,1) ;
        1  1           1            1 ] ;
% box2_ is the inverse of the best homography * box2
box2_ = inv(H) * box2 ;
% set the first 2 elements in box2_ to the ratio of the first two elements
% and the third
box2_(1,:) = box2_(1,:) ./ box2_(3,:) ;
box2_(2,:) = box2_(2,:) ./ box2_(3,:) ;
% ur is range of the minimum of box2_ x to the max of box2_ x
% vr is range of the minimum of box2_ y to the max of box2_ y
ur = min([1 box2_(1,:)]):max([size(im1,2) box2_(1,:)]) ;
vr = min([1 box2_(2,:)]):max([size(im1,1) box2_(2,:)]) ;
% replicate the grid vectors ur and vr to produce a full grid
[u,v] = meshgrid(ur,vr) ;
% change back to double with the new grid
im1_ = vl_imwbackward(im2double(im1),u,v) ;

z_ = H(3,1) * u + H(3,2) * v + H(3,3) ;
u_ = (H(1,1) * u + H(1,2) * v + H(1,3)) ./ z_ ;
v_ = (H(2,1) * u + H(2,2) * v + H(2,3)) ./ z_ ;
im2_ = vl_imwbackward(im2double(im2),u_,v_) ;
% make any "not a numbers" equal to 0
mass = ~isnan(im1_) + ~isnan(im2_) ;
im1_(isnan(im1_)) = 0 ;
im2_(isnan(im2_)) = 0 ;
% add the two images together accounting for the error mass
mosaic = (im1_ + im2_) ./ mass ;

if display == 1
    figure(2) ; clf ;
    imagesc(mosaic) ; axis image off ;
    title('Mosaic') ;
end

if nargout == 0, clear mosaic ; end

end