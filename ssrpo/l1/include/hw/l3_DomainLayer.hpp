#pragma once

#include <cassert>
#include <chrono>
#include <memory>
#include <vector>
#include <string>
#include "l4_InfrastructureLayer.hpp"



/**
 * Класс для представления продукта.
 * Наследуется от AppendableInterface.
 */
class Product final : public AppendableInterface {
    std::string _name;///< Имя продукта.
    unsigned int _cost;///< Стоимость продукта.
    unsigned int _count;///< Количество продукта.
    std::chrono::time_point<std::chrono::system_clock> _created_at;///< Время создания продукта.

protected:
    /**
     * Проверяет инвариант продукта.
     * @returns {bool} - Возвращает true, если состояние объекта корректно.
     */
    bool invariant() const;

public:
    Product() = delete; ///< Конструктор по умолчанию удалён.
    Product(const Product & p) {
        _name = p._name;
        _cost = p._cost;
        _count = p._count;
    } ///< Конструктор копирования удалён.
    Product &operator=(const Product &) = delete;///< Оператор присваивания удалён.

    /**
     * Конструктор с параметрами для создания продукта.
     * @param {std::string} product_name - Название продукта.
     * @param {unsigned int} product_cost - Стоимость продукта.
     * @param {unsigned int} count - Количество продукта.
     */
    Product(std::string product_name, unsigned int product_cost, unsigned int count) :
    _name(product_name), _cost(product_cost),
         _count(count) {
              assert(invariant());
         }

    /**
     * Получает имя продукта.
     * @returns {const std::string&} - Имя продукта.
     */
    const std::string &product_name() const;

    /**
     * Получает стоимость продукта.
     * @returns {unsigned int} - Стоимость продукта.
     */
    const unsigned int product_cost() const;

    /**
     * Получает количество продукта.
     * @returns {unsigned int} - Количество продукта.
     */
    unsigned int count() const;

    /**
     * Устанавливает новое количество продукта.
     * @param new_count Новое количество продукта.
     */
    void set_count(int new_count);

    /**
     * Устанавливает новое имя продукта.
     * @param new_cost Новое имя продукта (возможно, должно быть new_name).
     */
    void set_cost(int new_cost);

    /**
     * Устанавливает время создания продукта.
     * Переопределённый метод из AppendableInterface.
     * @param {std::chrono::time_point<std::chrono::system_clock>} time - Время создания продукта.
     */
    void set_created_at(
        std::chrono::time_point<std::chrono::system_clock> time) override;
};

typedef std::vector<std::shared_ptr<Product>> products;


/**
 * Класс для управления продуктами.
 */
class ProductManager {
    DataBase _db; ///< База данных для хранения продуктов.

public:
    /**
     * Конструктор для создания менеджера продуктов.
     * @param {DataBase} db - Объект базы данных.
     */
    explicit ProductManager(DataBase db) {
        _db = db;
    }

    /**
     * Добавляет продукт в базу данных.
     * @param {Product} product - Продукт для добавления.
     */
    void add_product(Product product);

    /**
     * Удаляет продукт из базы данных.
     * @param {Product} product - Продукт для удаления.
     */
    void delete_product(std::string product_name);

    /**
     * Получает все продукты из базы данных.
     * @returns {db_elements} - Список всех продуктов.
     */
    products get_all_products();;

    /**
     * Обновляет информацию о продукте в базе данных.
     * @param {Product} product - Продукт для обновления.
     */
    void update_product(Product product);

    /**
     * Получает продукт по его имени.
     * @param {std::string} product_name - Имя продукта для поиска.
     * @returns {std::shared_ptr<Product>} - Указатель на продукт, если найден, или nullptr.
     */
    std::shared_ptr<Product> get_product(std::string product_name);
};