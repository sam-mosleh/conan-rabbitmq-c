#include <iostream>
#include <amqp.h>
#include <amqp_tcp_socket.h>
#ifdef SAC_SSL_SUPPORT_ENABLED
#include <amqp_ssl_socket.h>
#endif
#include <amqp_framing.h>

int main(int argc, char const *argv[]) {
    amqp_connection_state_t conn = amqp_new_connection();
    std::cout << std::endl
              << "----------------->Tests are done for now.<---------------------" << std::endl
              << "///////////////////////////////////////////////////////////////" << std::endl;
    return 0;
}
