cmake_minimum_required(VERSION 3.8)
project(sentry_model_resources)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY resource
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
