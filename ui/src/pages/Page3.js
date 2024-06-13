import React, { useState } from 'react';
import { Form, Input, Button, Select, Table } from 'antd';
import './Page1.css';

const { Option } = Select;
const { TextArea } = Input;

const Page3 = () => {
  const [form] = Form.useForm();
  const [dataSource, setDataSource] = useState([]);

  const handleFinish = (values) => {
    setDataSource([
      ...dataSource,
      {
        key: dataSource.length,
        entity: values.entity_name,
        description: values.entity_description,
        category: values.entity_category,
      },
    ]);
    form.resetFields();
  };

  const handleCancel = () => {
    form.resetFields();
  };

  const columns = [
    {
      title: 'Entity',
      dataIndex: 'entity',
      key: 'entity',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Category',
      dataIndex: 'category',
      key: 'category',
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Button type="link" onClick={() => handleEdit(record.key)}>
          Edit
        </Button>
      ),
    },
  ];

  const handleEdit = (key) => {
    const record = dataSource.find((item) => item.key === key);
    form.setFieldsValue({
      entity_name: record.entity,
      entity_description: record.description,
      entity_category: record.category,
    });
    setDataSource(dataSource.filter((item) => item.key !== key));
  };

  return (
    <div>
      <h2>Sensitivity Score for Scheduled Runs</h2>
      <Form form={form} layout="vertical" onFinish={handleFinish}>
        <Form.Item
          label="Entity Name"
          name="entity_name"
          rules={[{ required: true, message: 'Please select an entity name!' }]}
        >
          <Select placeholder="Select an entity name">
            <Option value="Entity1">Entity1</Option>
            <Option value="Entity2">Entity2</Option>
            <Option value="Entity3">Entity3</Option>
          </Select>
        </Form.Item>
        <Form.Item
          label="Entity Category"
          name="entity_category"
          rules={[{ required: true, message: 'Please select an entity category!' }]}
        >
          <Select placeholder="Select an entity category">
            <Option value="Category1">Category1</Option>
            <Option value="Category2">Category2</Option>
            <Option value="Category3">Category3</Option>
          </Select>
        </Form.Item>
        <Form.Item
          label="Entity Description"
          name="entity_description"
          rules={[{ required: true, message: 'Please enter a description!' }]}
        >
          <TextArea rows={2} placeholder="Enter description" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
          <Button style={{ marginLeft: '10px' }} onClick={handleCancel}>
            Cancel
          </Button>
        </Form.Item>
      </Form>
      <Table columns={columns} dataSource={dataSource} />
    </div>
  );
};

export default Page3;
