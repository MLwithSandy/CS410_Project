docker volume create --driver local \
    --opt type=none \
    --opt device='/Users/sandeepkumar/Documents/04_Learning & Skills Improvement/MCS/Courses/CS410_TextInformationSystem/Project/CS410_Project/StockRatingsSystem/mongodbvol' \
    --opt o=bind mongodbvol