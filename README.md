# TgBotAnyDocumentToPDF
telegram bot that will convert documents to PDF format

# Docker
build image

` $ docker build -t name_your_image . `

you need to create a **.env** file and put the Telegram token there

`TOKEN = 'x0x0x0x0x0x0x0x0x0x0x0x0x0x0x--x0x0x0x0x--x0x0x'`

# Run container
` docker run -it -d name_your_image `

1. on your VDS, run the command
` wget https://github.com/JohnnnyBeGood/TgBotAnyDocumentToPDF/archive/refs/heads/main.zip `

2. in the folder **TgBotAnyDocumentToPDF-main** run the command ` touch .env `
3. to your file .env place a telegram token
4. starting the Docker container
` docker run -it -d name_your_image `