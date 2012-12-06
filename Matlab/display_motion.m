function motion = display_motion(dirImages, outDir)
tic;
if nargin == 0
    ERROR = 'Please input images'
    return
end
 

imageList = dir(fullfile(dirImages, '*.jpg'));

numOfImages = numel(imageList);

base = imread(fullfile(dirImages,imageList(1).name));
temp = imread(fullfile(dirImages,imageList(2).name));


motion = sift_motion(base,temp) ;




% Write the new mosaic image to the output file
imwrite(motion, outDir) ;

toc
end
