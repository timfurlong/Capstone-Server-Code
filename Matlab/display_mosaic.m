function mosaic = display_mosaic(dirImages, outDir, display)
tic;
if nargin == 0
    ERROR = 'Please input images'
    return
elseif nargin == 1
    display = 1;            
end

imageList = dir(fullfile(dirImages, '*.jpg'));

numOfImages = numel(imageList);

mosaic = imread(fullfile(dirImages,imageList(1).name));

for i = 2:numOfImages
    nextImage = imread(fullfile(dirImages,imageList(i).name));
    mosaic = sift_mosaic(mosaic, nextImage,display);    
end

% Write the new mosaic image to the output file
imwrite(mosaic, outDir) ;
toc

end
