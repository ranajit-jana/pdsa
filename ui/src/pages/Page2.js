import React, { useState } from 'react';
import { Form, Input, Button, Select, Table, Row, Col } from 'antd';
import './Page2.css';

const { Option } = Select;
const { TextArea } = Input;

const Page2 = () => {
  const [form] = Form.useForm();
  const [dataSource, setDataSource] = useState([]);

  const handleFinish = (values) => {
    setDataSource([
      ...dataSource,
      {
        key: dataSource.length,
        ruleName: values.rule_name,
        combination: values.entity_names.join(', '),
        description: values.rule_description,
        score: values.rule_score,
      },
    ]);
    form.resetFields();
  };

  const handleCancel = () => {
    form.resetFields();
  };

  const columns = [
    {
      title: 'Rule Name',
      dataIndex: 'ruleName',
      key: 'ruleName',
    },
    {
      title: 'Combination',
      dataIndex: 'combination',
      key: 'combination',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Score',
      dataIndex: 'score',
      key: 'score',
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
      rule_name: record.ruleName,
      rule_description: record.description,
      rule_score: record.score,
      entity_names: record.combination.split(', '),
    });
    setDataSource(dataSource.filter((item) => item.key !== key));
  };

  return (
    <div>
      <h2>PII Detection and Toxicity Analyzer</h2>
      <Form form={form} layout="vertical" onFinish={handleFinish}>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Rule Name"
              name="rule_name"
              rules={[{ required: true, message: 'Please enter a rule name!' }]}
            >
              <Input placeholder="Enter rule name" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Rule Category"
              name="rule_category"
              rules={[{ required: true, message: 'Please select a rule category!' }]}
            >
              <Select placeholder="Select a rule category">
                <Option value="Category1">Category1</Option>
                <Option value="Category2">Category2</Option>
                <Option value="Category3">Category3</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Rule Description"
              name="rule_description"
              rules={[{ required: true, message: 'Please enter a description!' }]}
            >
              <TextArea rows={2} placeholder="Enter description" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Rule Score"
              name="rule_score"
              rules={[{ required: true, message: 'Please select a score!' }]}
            >
              <Select placeholder="Select a score">
                {Array.from({ length: 10 }, (_, i) => (
                  <Option key={i + 1} value={i + 1}>{i + 1}</Option>
                ))}
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              label="Entities Names"
              name="entity_names"
              rules={[{ required: true, message: 'Please select entity names!' }]}
            >
              <Select mode="multiple" placeholder="Select entity names">
                <Option value="Entity1">Entity1</Option>
                <Option value="Entity2">Entity2</Option>
                <Option value="Entity3">Entity3</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Save
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

export default Page2;
