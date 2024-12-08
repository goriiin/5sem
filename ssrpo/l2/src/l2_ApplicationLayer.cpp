
#include "../include/hw/l3_DomainLayer.hpp"
#include <sstream>
#include "../include/hw/l2_ApplicationLayer.hpp"

const int PRODUCT_NAME_NUM = 1;
const int PRODUCT_COST_NUM = 2;
const int PRODUCT_COUNT_NUM = 3;

bool Application::run() {
     _io.output("для окончания e/end");
        _io.output("для создания продукта p/new <ИМЯ ПРОДУКТА> <ЦЕНА ПРОДУКТА> <КОЛИЧЕСТВО>");
        _io.output("для удаления продукта p/remove <ИМЯ ПРОДУКТА>");
        _io.output("для обновления продукта p/update <ИМЯ ПРОДУКТА> <НОВАЯ ЦЕНА> <НОВОЕ КОЛИЧЕСТВО>");
        _io.output("для создания клиента c/new <ИМЯ> <ФАМИЛИЯ> <EMAIL>");
        _io.output("для удаления клиента c/remove <ИМЯ ФАМИЛИЯ>");
        _io.output("для вывода всех клиентов c/view_all");
        _io.output("для создания заказа o/new_order <ИМЯ КЛИЕНТА> <АДРЕС ДОСТАВКИ>");
        _io.output("для добавления продукта в заказ o/add_product <НОМЕР ЗАКАЗА> <НАЗВАНИЕ ПРОДУКТА> <ЦЕНА>");
        _io.output("для вывода всех заказов o/view_all_orders");

        while (true) {
            auto user_input = _io.input();

            if (user_input.empty()) {
                _io.output("Нет введённых данных.");
                break;
            }

            if (user_input[0] == "e" || user_input[0] == "end") {
                _io.output("Ввод завершен");
                break;
            }

            if (user_input[0] == "p/new") {
                if (user_input.size() < 4) {
                    _io.output("Недостаточно данных для создания продукта.");
                    continue;
                }
                std::string name = user_input[1];
                unsigned int cost = std::stoul(user_input[2]);
                unsigned int count = std::stoul(user_input[3]);
                Product product(name, cost, count);
                _product_manager.add_product(product);
                _io.output("Продукт успешно добавлен.");
            }

            else if (user_input[0] == "p/remove") {
                if (user_input.size() < 2) {
                    _io.output("Недостаточно данных для удаления продукта.");
                    continue;
                }
                std::string name = user_input[1];
                _product_manager.delete_product(name);
                _io.output("Продукт успешно удалён.");
            }

            else if (user_input[0] == "p/update") {
                if (user_input.size() < 4) {
                    _io.output("Недостаточно данных для обновления продукта.");
                    continue;
                }
                std::string name = user_input[1];
                unsigned int new_cost = std::stoul(user_input[2]);
                unsigned int new_count = std::stoul(user_input[3]);
                Product product(name, new_cost, new_count);
                _product_manager.update_product(product);
                _io.output("Продукт успешно обновлён.");
            }

            else if (user_input[0] == "c/new") {
                if (user_input.size() < 4) {
                    _io.output("Недостаточно данных для создания клиента.");
                    continue;
                }

                std::string first_name = user_input[1];
                std::string last_name = user_input[2];
                std::string email = user_input[3];
                Person person(first_name, last_name, email);
                _person_manager.add_person(person);

                _io.output("Клиент успешно добавлен: " + first_name + " " + last_name + " " + email);
            }

            else if (user_input[0] == "c/remove") {
                if (user_input.size() < 3) {
                    _io.output("Недостаточно данных для удаления клиента.");
                    continue;
                }

                std::string full_name = user_input[1] + " " + user_input[2];
                _person_manager.delete_person(full_name);
                _io.output("Клиент " + full_name + " успешно удалён.");
            }

            else if (user_input[0] == "c/view_all") {
                auto all_persons = _person_manager.get_all_persons();
                if (all_persons.empty()) {
                    _io.output("Нет доступных клиентов.");
                    continue;
                }
                for (const auto& person : all_persons) {
                    std::stringstream ss;

                    ss << "customer: " << person->get_first_name()
                        << " " << person->get_last_name()
                        << " " << person->get_email();

                    _io.output(ss.str());
                }
            }

            else if (user_input[0] == "o/new_order") {
                if (user_input.size() < 3) {
                    _io.output("Недостаточно данных для создания заказа.");
                    continue;
                }
                std::string customer_name = user_input[1] + " " + user_input[2];
                std::string delivery_address = user_input[3];
                if (auto customer = _person_manager.get_person(customer_name)) {
                    Order order(customer, delivery_address);
                    int current_order_id = this->order_counter.fetch_add(1);
                    _order_manager.add_order(order, current_order_id);
                    _io.output("Заказ успешно создан.");
                } else {
                    _io.output("Клиент не найден.");
                }
            }

            else if (user_input[0] == "o/add_product") {
                if (user_input.size() < 4) {
                    _io.output("Недостаточно данных для добавления продукта в заказ.");
                    continue;
                }
                int order_id = std::stoi(user_input[1]);
                std::string product_name = user_input[2];
                unsigned int product_price = std::stoul(user_input[3]);
                if (auto order = _order_manager.get_order(order_id)) {
                    auto product = std::make_shared<Product>(product_name, product_price, 1);
                    order->add_product(product);
                    _io.output("Продукт добавлен в заказ.");
                } else {
                    _io.output("Заказ не найден.");
                }
            }

            else if (user_input[0] == "o/view_all_orders") {
                auto all_orders = _order_manager.get_all_orders();
                if (all_orders.empty()) {
                    _io.output("Нет доступных заказов.");
                    continue;
                }
                for (const auto& order : all_orders){
                    _io.output(order->get_info());
                }
            }

            else {
                _io.output("Недопустимая команда '" + user_input[0] + "'");
            }
        }

        return true;
    }


std::atomic<int> Application::order_counter{0};