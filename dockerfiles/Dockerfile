version: '2'
services:
  expressionbrowser:
      build: .
      restart: always
      ports:
          - "8003:80"
      depends_on:
          - expressionbrowserdb
      volumes:
          - ./data/:/db

  expressionbrowserdb:
    image: mariadb
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=admin
      - MYSQL_DATABASE=db
      - MYSQL_USER=myuser
      - MYSQL_PASSWORD=mypassword
    ports:
      - "3306:3306"
    volumes:
      - ./mysql/:/docker-entrypoint-initdb.d

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    restart: always
    depends_on:
      - expressionbrowserdb
    ports:
      - 8182:80
    environment:
      PMA_USER: root
      PMA_PASSWORD: admin
      PMA_ARBITRARY: 1
