#include <iostream>
#include <string>
#include <fmt/core.h>

std::string getKey(std::string dev, std::string ip, std::string name) {
  return fmt::format(fmt::runtime("{}_{},{}"), dev, ip, name);
}

int main() {
  std::cout << "Hello world\n";
  std::cout << std::string("foo") << "\n";

  std::string dev = "iPhone14,5";
  std::string ip = "nnn.nnn.nnn.nnn";
  std::string name = "testpipeline";
  std::string data = "{\"1\":2,\"3\":7}";
  std::string dataWrap = fmt::format(fmt::runtime("{{\"value\":{}}}"), data);
  
  std::cout << dataWrap << "\n";
  std::cout << getKey(dev, ip, name) << "\n";
  return 0;
}
